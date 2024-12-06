import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Optional, Tuple, Dict

import requests
from psycopg2 import pool
from psycopg2.extras import execute_batch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Neynar API configuration
API_URL = "https://api.warpcast.com/fc/blocked-users"
# PostgreSQL configuration
PG_CONFIG = {

}
BATCH_SIZE = 1000
MAX_RETRIES = 10
BACKOFF_FACTOR = 0.75
MAX_WORKERS = os.cpu_count() * 10  # Number of threads for parallel processing


def create_session_with_retries() -> requests.Session:
    """Creates a session with retry logic for robust HTTP requests."""
    session = requests.Session()
    retries = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


def fetch_data(session: requests.Session, blocker_fid: int, cursor: Optional[str] = None) -> Optional[Dict]:
    """Fetch data for a specific blockerFid with optional pagination."""
    params = {"blockerFid": blocker_fid, "cursor": cursor} if cursor else {"blockerFid": blocker_fid}
    retry = 5
    while retry > 0:
        try:
            response = session.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data for blockerFid {blocker_fid}: {e}")
        retry -= 1
        time.sleep(5)
    return None


def fetch_blocks(session: requests.Session, blocker_fid: int) -> List[Tuple]:
    """Fetch all blocks for a given blockerFid, handling pagination."""
    blocks = []
    cursor = None
    while True:
        data = fetch_data(session, blocker_fid, cursor)
        if not data or "result" not in data:
            break
        new_blocks, cursor = parse_json(data)
        blocks.extend(new_blocks)
        if not cursor:  # No more pages
            break
    return blocks


def parse_json(data: Dict) -> Tuple[List[Tuple], Optional[str]]:
    """Parse JSON response into a list of block records."""
    blocks = [
        (
            block["blockerFid"],
            block["blockedFid"],
            datetime.utcfromtimestamp(block["createdAt"]),
            datetime.now(),  # created_at
            datetime.now(),  # updated_at
        )
        for block in data["result"]["blockedUsers"]
    ]
    return blocks, data.get("next", {}).get("cursor")


def insert_blocks(connection_pool, blocks: List[Tuple]) -> None:
    """Insert block records into the database in batches."""
    query = """
    INSERT INTO farcaster_blocks (
        blocker_fid, blocked_fid, blocked_at, created_at, updated_at
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (blocker_fid, blocked_fid) DO UPDATE SET
        blocked_at = EXCLUDED.blocked_at,
        updated_at = EXCLUDED.updated_at;
    """
    try:
        conn = connection_pool.getconn()
        with conn.cursor() as cur:
            execute_batch(cur, query, blocks, page_size=BATCH_SIZE)
        conn.commit()
    except Exception as e:
        print(f"Database error during batch insert: {e}")
        conn.rollback()
    finally:
        if conn:
            connection_pool.putconn(conn)


def process_fids_in_batches(connection_pool, session: requests.Session, fids: List[int]) -> None:
    """Fetch and store block data for multiple blockerFids in parallel."""
    total_inserted = 0
    for i in range(0, len(fids), 1000):  # Process in smaller batches
        batch_fids = fids[i:i + 1000]
        blocks = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(fetch_blocks, session, fid): fid for fid in batch_fids}
            for future in as_completed(futures):
                try:
                    blocks.extend(future.result())
                except Exception as e:
                    print(f"Error processing blockerFid {futures[future]}: {e}")

        if blocks and len(blocks) > 0:
            insert_blocks(connection_pool, blocks)
            total_inserted += len(blocks)
        print(f"Inserted {len(blocks)} blocks for batch starting with blockerFid {batch_fids[0]}")

    print(f"Total blocks inserted: {total_inserted}")


def main():
    """Main function to manage the process."""
    connection_pool = None
    try:
        connection_pool = pool.SimpleConnectionPool(1, 10, **PG_CONFIG)
        session = create_session_with_retries()
        blocker_fids = list(range(742001, 890000))  # Replace with actual FIDs
        process_fids_in_batches(connection_pool, session, blocker_fids)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection_pool:
            connection_pool.closeall()


if __name__ == "__main__":
    main()
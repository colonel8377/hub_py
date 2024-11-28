import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests
import psycopg2
from psycopg2.extras import execute_batch
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Neynar API configuration
API_URL = "https://api.neynar.com/v2/farcaster/block/list"
HEADERS = {
    "accept": "application/json",
    "x-neynar-experimental": "true",
    "x-api-key": "NEYNAR_API_DOCS"
}

# PostgreSQL configuration
PG_CONFIG = {
    "dbname": "",
    "user": "",
    "password": "",
    "host": "",
    "port": 6541
}
BATCH_SIZE = 1000
MAX_RETRIES = 5
BACKOFF_FACTOR = 0.5
REQUEST_LIMIT = 300
TIME_PERIOD = 60  # seconds

def create_session_with_retries():
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

def fetch_data(session, blocker_fid, cursor=None, limit=100):
    params = {"blocker_fid": blocker_fid, "limit": limit}
    if cursor:
        params["cursor"] = cursor
    while True:
        try:
            response = session.get(API_URL, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if response.status_code == 429 and response.json().get("code") == "RateLimitExceeded":
                print("Rate limit exceeded. Sleeping for 60 seconds...")
                time.sleep(TIME_PERIOD)
            else:
                print(f"HTTP error for fid {blocker_fid}: {e}")
                return None
        except requests.RequestException as e:
            print(f"Request error for fid {blocker_fid}: {e}")
            return None

def fetch_all_blocks(session, blocker_fid):
    blocks = []
    cursor = None
    while True:
        data = fetch_data(session, blocker_fid, cursor)
        if not data or "blocks" not in data:
            break
        blocks.extend(parse_json(data, blocker_fid))
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return blocks

def parse_json(data, blocker_fid):
    blocks = []
    for block in data["blocks"]:
        blocked = block["blocked"]
        blocks.append((
            blocker_fid,
            blocked["fid"],
            block["blocked_at"],
            datetime.now(),  # created_at
            datetime.now()   # updated_at
        ))
    return blocks

def insert_data(conn, blocks):
    block_query = """
    INSERT INTO farcaster_blocks (
        blocker_fid, blocked_fid, blocked_at, created_at, updated_at
    ) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (blocker_fid, blocked_fid) DO UPDATE SET
        blocked_at = EXCLUDED.blocked_at,
        updated_at = EXCLUDED.updated_at;
    """
    try:
        with conn.cursor() as cur:
            if blocks:
                execute_batch(cur, block_query, blocks)
            conn.commit()
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
        conn.rollback()

def main(blocker_fids):
    conn = None
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        session = create_session_with_retries()
        insert_datas = []
        with session as session:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = {
                    executor.submit(fetch_all_blocks, session, blocker_fid): blocker_fid
                    for blocker_fid in blocker_fids
                }
                for future in as_completed(futures):
                    block_data = future.result()
                    insert_datas.extend(block_data)
                    if len(insert_datas) >= BATCH_SIZE:
                        insert_data(conn, insert_datas)
                        insert_datas.clear()
        if insert_datas:
            insert_data(conn, insert_datas)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main([i for i in range(1, 890000)])  # Example blocker FIDs
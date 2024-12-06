from typing import Tuple, List

import requests
import psycopg2
from datetime import datetime
import traceback


from psycopg2.extras import execute_batch
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# Database connection details
DB_CONFIG = {
    "dbname": "DappResearch",
    "user": "DappResearch",
    "password": "FarcasterIndexer",
    "host": "100.81.228.99",
    "port": 6541
}

# API endpoint and headers
API_URL = "https://api.warpcast.com/fc/channel-restricted-users"
HEADERS = {
    "Content-Type": "application/json"
}
BATCH_SIZE = 1000


def create_session_with_retries():
    session = requests.Session()
    retries = Retry(
        total=10,
        backoff_factor=0.75,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    return session


def insert_data(conn, blocks: List[Tuple]) -> None:
    query = """
                INSERT INTO restricted_users (fid, channel_id, restricted_at, created_at, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT (fid, channel_id)
                DO UPDATE SET
                    restricted_at = EXCLUDED.restricted_at,
                    updated_at = CURRENT_TIMESTAMP;
            """

    try:
        with conn.cursor() as cur:
            execute_batch(cur, query, blocks)
        conn.commit()
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        print(f"Database error during insert: {traceback_str}")
        conn.rollback()


def fetch_and_store_bans():
    cursor = None
    session = create_session_with_retries()
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        blocks = []
        l = 0
        # Fetch data from API
        params = {}
        while True:
            response = session.get(API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse and insert data into PostgreSQL
            banned_users = data["result"]["restrictedUsers"]
            for user in banned_users:
                fid = user["fid"]
                channel_id = user["channelId"]
                restricted_at = datetime.utcfromtimestamp(user['restrictedAt'])

                blocks.append((fid, channel_id, restricted_at))

                if len(blocks) >= BATCH_SIZE:
                    insert_data(conn, blocks)
                    l += len(blocks)
                    print(f"Inserted {l} blocks")
                    blocks.clear()
                # Insert into table


            # Commit transaction
            conn.commit()
            # Handle pagination
            next_cursor = data.get("next", {}).get("cursor")
            if not next_cursor:
                break
            params["cursor"] = next_cursor
        if len(blocks) >= BATCH_SIZE:
            insert_data(conn, blocks)
            l += len(blocks)
            print(f"Inserted {l} blocks")
            blocks.clear()
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        # Close database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    fetch_and_store_bans()
import os
from datetime import datetime

import requests
import psycopg2
from psycopg2.extras import execute_values
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration
API_URL = "https://api.warpcast.com/fc/account-verifications"
POSTGRES_CONFIG = {
}
MAX_RETRIES = 10
THREADS = os.cpu_count() * 10
BATCH_SIZE = 10000  # Number of rows per batch before insertion

# Retry logic session
def create_session_with_retries():
    session = requests.Session()
    retries = requests.adapters.Retry(
        total=MAX_RETRIES,
        backoff_factor=0.75,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Fetch data from the API
def fetch_data(session, cursor=None):
    params = {"cursor": cursor} if cursor else {}
    print(f"Fetching data with cursor: {cursor}")
    response = session.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

# Store data in PostgreSQL in bulk
def batch_upsert_to_db(data):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO account_verifications (
            fid, platform, platform_id, platform_username, verified_at, created_at, updated_at
        )
        VALUES %s
        ON CONFLICT (fid, platform_id) DO UPDATE SET
            platform = EXCLUDED.platform,
            platform_username = EXCLUDED.platform_username,
            verified_at = EXCLUDED.verified_at,
            updated_at = EXCLUDED.updated_at;
        """
        print(f"Batch inserting {len(data)} rows into the database.")
        records = [
            (
                v["fid"], v["platform"], v["platformId"], v["platformUsername"],
                datetime.utcfromtimestamp(v["verifiedAt"]), datetime.utcnow(), datetime.utcnow()
            )
            for v in data
        ]
        execute_values(cursor, insert_query, records)
        conn.commit()
        print(f"Batch of {len(data)} rows inserted successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error during batch upsert: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Process a round of data fetching and batching
def process_round(session, cursor):
    buffer = []  # Accumulate data in this buffer
    next_cursor = cursor
    while True:
        try:
            response = fetch_data(session, next_cursor)
            verifications = response["result"]["verifications"]
            buffer.extend(verifications)
            print(f"Fetched {len(verifications)} verifications. Buffer size: {len(buffer)}")
            next_cursor = response["next"].get("cursor") if "next" in response else None

            # Check if the buffer size has reached the batch size
            if len(buffer) >= BATCH_SIZE:
                batch_upsert_to_db(buffer[:BATCH_SIZE])  # Upsert the first batch
                buffer = buffer[BATCH_SIZE:]  # Retain the rest in the buffer

            # Exit if no more data
            if not next_cursor:
                break

        except Exception as e:
            print(f"Error during data fetching or processing: {e}")
            break

    # Insert remaining data in the buffer
    if buffer:
        print(f"Final batch of {len(buffer)} rows being upserted.")
        batch_upsert_to_db(buffer)

# Main function
def main():
    print("Starting data ingestion process with round-based batching...")
    session = create_session_with_retries()
    cursor = None

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.submit(process_round, session, cursor)

if __name__ == "__main__":
    start_time = time.time()
    try:
        main()
        print(f"Data ingestion completed successfully in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        print("Program terminated.")
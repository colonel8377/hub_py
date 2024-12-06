import requests
import psycopg2
from datetime import datetime

# Database connection details
DB_CONFIG = {
}

# API endpoint and headers
API_URL = "https://api.warpcast.com/fc/channel-bans"
HEADERS = {
    "Content-Type": "application/json"
}

def fetch_and_store_bans():
    cursor = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch data from API
        params = {}
        while True:
            response = requests.get(API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            # Parse and insert data into PostgreSQL
            banned_users = data["result"]["bannedUsers"]
            for user in banned_users:
                fid = user["fid"]
                channel_id = user["channelId"]
                banned_at = datetime.utcfromtimestamp(user["bannedAt"])

                # Insert into table
                cursor.execute("""
                                    INSERT INTO banned_users (fid, channel_id, banned_at, created_at, updated_at)
                                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                                    ON CONFLICT (fid, channel_id)
                                    DO UPDATE SET
                                        banned_at = EXCLUDED.banned_at,
                                        updated_at = CURRENT_TIMESTAMP;
                                """, (fid, channel_id, banned_at))

            # Commit transaction
            conn.commit()

            # Handle pagination
            next_cursor = data.get("next", {}).get("cursor")
            if not next_cursor:
                break
            params["cursor"] = next_cursor

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
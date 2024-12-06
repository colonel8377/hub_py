import logging
import threading
import time
from datetime import datetime
from queue import Queue

import psycopg2
import requests
from psycopg2.extras import execute_batch
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# Configure logging
logging.basicConfig(level=logging.ERROR, format="[%(asctime)s] %(levelname)s: %(message)s")

DB_CONFIG = {

}

API_URL = "https://client.warpcast.com/v2/user-by-fid?fid={}"
MAX_RETRIES = 20
RETRY_BACKOFF = 2
THREAD_POOL_SIZE = 50 # Number of threads for parallel processing
BATCH_SIZE = 100  # Number of records per database batch


def parse_timestamp(timestamp):
    """Convert a millisecond timestamp to a UTC datetime."""
    return datetime.utcfromtimestamp(timestamp / 1000) if timestamp else None


def fetch_user_profile(fid, max_retries=5, retry_backoff=2,):
    """
    Fetch user profile from the API with retries and proxy support.

    Args:
        fid (int): User's unique identifier.
        proxies (dict): Proxy configuration for the request.
        max_retries (int): Maximum number of retries.
        retry_backoff (float): Backoff factor for retries.
        api_url (str): URL template for the API endpoint.

    Returns:
        dict: User profile data if successful.
        None: If the request fails or the user is not found.
    """
    url = API_URL.format(fid)
    # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=retry_backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=10)  # Setting timeout for better resilience
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            logging.error(f"User with fid {fid} not found (400).")
            return None
        else:
            logging.error(f"Failed to fetch fid {fid}: {response.status_code} - {response.reason}; url: {url}")
            logging.error(f"Response content: {response.text}")
    except requests.RequestException as e:
        logging.error(f"Error fetching fid {fid}: {e}")

    return None


def store_profiles_batch(conn, profiles):
    """Store multiple user profiles into the database in a batch."""
    if not profiles:
        return

    users_data, bios_data, streaks_data = [], [], []

    for profile in profiles:
        user = profile.get("result", {}).get("user", {})
        if not user or not user.get("fid"):
            continue

        # Users table
        users_data.append((
            user["fid"],
            user.get("username", None),
            user.get("displayName", None),
            user.get("pfp", {}).get("url"),
            user.get("pfp", {}).get("verified", False),
            user.get("followerCount", None),
            user.get("followingCount", None),
            user.get("activeOnFcNetwork", False),
        ))

        # Profiles table (bios)
        profile_data = user.get("profile", {})
        if profile_data:
            bios_data.append((
                user["fid"],
                profile_data.get("bio", {}).get("text"),
                profile_data.get("bio", {}).get("mentions", []),
                profile_data.get("bio", {}).get("channelMentions", []),
                profile_data.get("location", {}).get("description"),
                profile_data.get("location", {}).get("placeId"),
            ))

        # Streaks table
        streak = user.get("streak", {})
        if streak:
            channel = streak.get("channel", {})
            metadata = streak.get("metadata", {})
            streaks_data.append((
                user["fid"],
                channel.get("key"),
                channel.get("name"),
                channel.get("imageUrl"),
                channel.get("description"),
                channel.get("followerCount"),
                streak.get("streakCount"),
                metadata.get("alreadyCastedToday"),
                parse_timestamp(metadata.get("startedAtTimestamp")),
                parse_timestamp(metadata.get("expiresAtTimestamp")),
                parse_timestamp(metadata.get("latestWindowStartTimestamp")),
                metadata.get("latestWindowCastCount"),
            ))

    # Execute batch upserts for each table
    with conn.cursor() as cursor:
        if users_data:
            try:
                execute_batch(cursor, """
                    INSERT INTO warpcast_users (
                        fid, username, display_name, profile_image_url, profile_image_verified,
                        follower_count, following_count, active_on_fc_network
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (fid) DO UPDATE
                    SET username = EXCLUDED.username,
                        display_name = EXCLUDED.display_name,
                        profile_image_url = EXCLUDED.profile_image_url,
                        profile_image_verified = EXCLUDED.profile_image_verified,
                        follower_count = EXCLUDED.follower_count,
                        following_count = EXCLUDED.following_count,
                        active_on_fc_network = EXCLUDED.active_on_fc_network;
                """, users_data)
                conn.commit()
            except Exception as e:
                logging.error(f"Failed to insert data into warpcast_users: {e}")
                conn.rollback()

        if bios_data:
            try:
                execute_batch(cursor, """
                INSERT INTO warpcast_bios (
                    fid, bio_text, mentions, channel_mentions, location_description, location_place_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (fid) DO UPDATE
                SET bio_text = EXCLUDED.bio_text,
                    mentions = EXCLUDED.mentions,
                    channel_mentions = EXCLUDED.channel_mentions,
                    location_description = EXCLUDED.location_description,
                    location_place_id = EXCLUDED.location_place_id;
                """, bios_data)
                conn.commit()
            except Exception as e:
                logging.error(f"Failed to insert data into warpcast_bios: {e}")
                conn.rollback()


        if streaks_data:
            try:
                execute_batch(cursor, """
                    INSERT INTO warpcast_streaks (
                        fid, channel_key, channel_name, channel_image_url, channel_description,
                        channel_follower_count, streak_count, already_casted_today,
                        started_at, expires_at, latest_window_start_at, latest_window_cast_count
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (fid) DO UPDATE
                    SET channel_key = EXCLUDED.channel_key,
                        channel_name = EXCLUDED.channel_name,
                        channel_image_url = EXCLUDED.channel_image_url,
                        channel_description = EXCLUDED.channel_description,
                        channel_follower_count = EXCLUDED.channel_follower_count,
                        streak_count = EXCLUDED.streak_count,
                        already_casted_today = EXCLUDED.already_casted_today,
                        started_at = EXCLUDED.started_at,
                        expires_at = EXCLUDED.expires_at,
                        latest_window_start_at = EXCLUDED.latest_window_start_at,
                        latest_window_cast_count = EXCLUDED.latest_window_cast_count;
                """, streaks_data)
                conn.commit()
            except Exception as e:
                logging.error(f"Failed to insert data into warpcast_streaks: {e}")
                conn.rollback()


# Thread Initialization
def initialize_threads(total_ids):
    """Initializes and starts threads for project processing."""
    jobs = []
    handler_map = {i: total_ids[i::THREAD_POOL_SIZE] for i in range(THREAD_POOL_SIZE)}
    for i in range(THREAD_POOL_SIZE):
        thread = threading.Thread(target=process_fids, args=(i, handler_map))
        jobs.append(thread)
        thread.start()
    return jobs


def process_fids(thread_id, handler_map):
    """Fetch and store profiles for a list of FIDs using threads."""
    # with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
    # futures = {executor.submit(fetch_user_profile, fid): fid for fid in fids}
    for fid in handler_map.get(thread_id, []):
        profile = fetch_user_profile(fid)
        if profile:
            sharable_queue.put(profile)


# Consumer Thread
def consumer(conn):
    batch = []
    total_processed = 0
    while True:
        try:
            profile = sharable_queue.get()
            if profile is None:  # Stop signal
                break
            if profile:
                batch.append(profile)
            if len(batch) >= BATCH_SIZE:
                store_profiles_batch(conn, batch)
                total_processed += len(batch)
                print(f'Pocessed {total_processed} profiles')
                batch.clear()
            time.sleep(1)
        finally:
            sharable_queue.task_done()
    if batch:
        store_profiles_batch(conn, batch)
        total_processed += len(batch)
        print(f'Pocessed {total_processed} profiles')
        batch.clear()

if __name__ == "__main__":
    fids = []
    sharable_queue = Queue()
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("select fid from warpcast_users group by fid")
    results = cursor.fetchall()
    cursor.close()
    processed_fid = [i[0] for i in results]
    fids = []
    for id in range(1, 890000):
        if id in processed_fid:
            continue
        fids.append(id)
    print(f'Processing {len(fids)} profiles')
    # Start consumer thread
    consumer_thread = threading.Thread(target=consumer, args=(conn,))
    consumer_thread.start()

    # Start worker threads
    threads = initialize_threads(fids)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Signal consumer thread to stop
    sharable_queue.put(None)
    consumer_thread.join()
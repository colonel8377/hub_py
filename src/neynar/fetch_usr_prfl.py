import json
import os
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import closing

import psycopg2
import requests
from psycopg2.extras import execute_values
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

from src.examples.utils import get_env_client
from src.hub_py.generated.request_response_pb2 import FidRequest

# Database Configuration
DB_CONFIG = {
    "database": "",
    "user": "",
    "password": "",
    "host": "",
    "port": "6541",
}

# API Configuration
BASE_URL = "https://api.neynar.com/v2/farcaster/user/by_username"
HEADERS = {
    "accept": "application/json",
    "x-neynar-experimental": "true",
    "x-api-key": "B5F14029-CFF6-47F1-97FD-F6BC7866EC37",
}
BATCH_SIZE = 1000
MAX_RETRIES = 5
BACKOFF_FACTOR = 0.5


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


def fetch_user_data(session, username):
    url = f"{BASE_URL}?username={username}"
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json().get("user")
    except RequestException as e:
        print(f"Error fetching data for {username}: {e}")
    return None


def batch_upsert(conn, users_data):
    insert_query = """
    INSERT INTO user_profile (
        fid, username, display_name, pfp_url, custody_address, profile,
        follower_count, following_count, power_badge, neynar_user_score
    )
    VALUES %s
    ON CONFLICT (fid) DO UPDATE SET
        username = EXCLUDED.username,
        display_name = EXCLUDED.display_name,
        pfp_url = EXCLUDED.pfp_url,
        custody_address = EXCLUDED.custody_address,
        profile = EXCLUDED.profile,
        follower_count = EXCLUDED.follower_count,
        following_count = EXCLUDED.following_count,
        power_badge = EXCLUDED.power_badge,
        neynar_user_score = EXCLUDED.neynar_user_score;
    """
    user_values = [
        (
            user["fid"],
            user["username"],
            user["display_name"],
            user["pfp_url"],
            user["custody_address"],
            json.dumps(user.get("profile", {})),
            user.get("follower_count", 0),
            user.get("following_count", 0),
            user.get("power_badge", False),
            user.get("experimental", {}).get("neynar_user_score", 0),
        )
        for user in users_data
    ]
    with conn.cursor() as cursor:
        execute_values(cursor, insert_query, user_values)
        conn.commit()


def fetch_username_by_fid(fid):
    try:
        client = get_env_client(use_async=False)
        request = FidRequest(fid=fid, page_size=50)
        msg_resp = client.GetAllUserDataMessagesByFid(request)
        for message in msg_resp.messages:
            if message.data.user_data_body.type == 6:  # Username type
                return fid, message.data.user_data_body.value
    except Exception as e:
        print(f"Failed to fetch username for fid {fid}: {e}")
    return fid, None


def fetch_usernames(fids):
    usernames = {}
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(fetch_username_by_fid, fid): fid for fid in fids}
        for future in as_completed(futures):
            fid, username = future.result()
            if username:
                usernames[fid] = username
    return usernames


def process_users(usernames):
    session = create_session_with_retries()
    all_users_data = []
    failure_users = []

    with closing(psycopg2.connect(**DB_CONFIG)) as conn:
        with session as session:
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                futures = {
                    executor.submit(fetch_user_data, session, username): fid
                    for fid, username in usernames.items()
                }
                for future in as_completed(futures):
                    user_data = future.result()
                    if user_data:
                        all_users_data.append(user_data)
                    else:
                        failure_users.append(usernames[futures[future]])

                    if len(all_users_data) >= BATCH_SIZE:
                        batch_upsert(conn, all_users_data)
                        all_users_data.clear()

        if all_users_data:
            batch_upsert(conn, all_users_data)

    return failure_users


if __name__ == "__main__":
    try:
        fids = range(1, 890000)
        print("Fetching usernames...")
        usernames = fetch_usernames(fids)
        with open("../../data/username_map.pkl", "wb") as f:
            pickle.dump(usernames, f)
        print(f"Fetched {len(usernames)} usernames. Fetching user profiles...")
        failures = process_users(usernames)
        with open("../../data/failure_username.pkl", "wb") as f:
            pickle.dump(failures, f)
        print("Completed fetching user profiles.")
    except Exception as e:
        print(f"An error occurred: {e}")
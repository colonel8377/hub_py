import logging
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
import psycopg2
from psycopg2.extras import execute_values
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# PostgreSQL connection details
DB_CONFIG = {
}

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def create_tables():
    ddl = """
    CREATE TABLE IF NOT EXISTS channels (
        id TEXT PRIMARY KEY,
        name TEXT,
        url TEXT,
        description TEXT,
        description_mentions INTEGER[],
        description_mentions_positions INTEGER[],
        image_url TEXT,
        header_image_url TEXT,
        lead_fid INTEGER,
        followed_at TIMESTAMP,
        follower_count INTEGER,
        member_count INTEGER,
        pinned_cast_hash TEXT,
        public_casting BOOLEAN,
        external_link_title TEXT,
        external_link_url TEXT,
        moderatorFids INTEGER[],
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS channel_followers (
        id SERIAL PRIMARY KEY,
        channel_id TEXT REFERENCES channels(id),
        fid INTEGER,
        followed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (channel_id, fid)
    );
    """
    execute_db_query(ddl)
    logging.info("Database tables created or already exist.")


def execute_db_query(query, data=None):
    """Reusable function to execute a query."""
    if not data:
        return
    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            if data:
                execute_values(cur, query, data)
            else:
                cur.execute(query)
    conn.close()


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


def fetch_and_store_channels(is_store: bool):
    logging.info("Fetching channels from API...")
    api_url = "https://api.warpcast.com/v2/all-channels"
    response = requests.get(api_url)
    response.raise_for_status()
    channels = response.json()['result']['channels']
    logging.info(f"Fetched {len(channels)} channels.")

    channel_data = [
        (
            channel['id'],
            channel['name'],
            channel['url'],
            channel.get('description'),
            channel.get('descriptionMentions'),
            channel.get('descriptionMentionsPositions'),
            channel.get('imageUrl'),
            channel.get('headerImageUrl'),
            channel.get('leadFid'),
            datetime.utcfromtimestamp(channel['createdAt']),
            channel.get('followerCount'),
            channel.get('memberCount'),
            channel.get('pinnedCastHash'),
            channel.get('publicCasting'),
            channel.get('externalLink', {}).get('title'),
            channel.get('externalLink', {}).get('url'),
            channel.get('moderatorFids'),
            datetime.utcnow(),
            datetime.utcnow(),
        )
        for channel in channels
    ]

    query = """
        INSERT INTO channels (
            id, name, url, description, description_mentions, description_mentions_positions,
            image_url, header_image_url, lead_fid, followed_at, follower_count, member_count, 
            pinned_cast_hash, public_casting, external_link_title, external_link_url, moderatorFids,
            created_at, updated_at
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            url = EXCLUDED.url,
            description = EXCLUDED.description,
            description_mentions = EXCLUDED.description_mentions,
            description_mentions_positions = EXCLUDED.description_mentions_positions,
            image_url = EXCLUDED.image_url,
            header_image_url = EXCLUDED.header_image_url,
            lead_fid = EXCLUDED.lead_fid,
            followed_at = EXCLUDED.followed_at,
            follower_count = EXCLUDED.follower_count,
            member_count = EXCLUDED.member_count,
            pinned_cast_hash = EXCLUDED.pinned_cast_hash,
            public_casting = EXCLUDED.public_casting,
            external_link_title = EXCLUDED.external_link_title,
            external_link_url = EXCLUDED.external_link_url,
            moderatorFids = EXCLUDED.moderatorFids,
            updated_at = EXCLUDED.updated_at
    """
    if is_store:
        execute_db_query(query, channel_data)
        logging.info("Channels stored in database.")
    return [channel['id'] for channel in channels]  # Return channel IDs for next step


def fetch_and_store_followers(session, channel_id):
    logging.info(f"Fetching followers for channel: {channel_id}")
    api_url = f"https://api.warpcast.com/v1/channel-followers?channelId={channel_id}"
    followers = []
    count = 0

    while api_url:
        response = session.get(api_url)
        response.raise_for_status()
        data = response.json()
        followers.extend(data['result']['users'])
        count += len(data['result']['users'])

        next_cursor = data.get('next', {}).get('cursor')
        api_url = f"https://api.warpcast.com/v1/channel-followers?channelId={channel_id}&cursor={next_cursor}" if next_cursor else None

    logging.info(f"Fetched {count} followers for channel: {channel_id}")

    follower_data = [
        (channel_id, follower['fid'], datetime.utcfromtimestamp(follower['followedAt']), datetime.utcnow())
        for follower in followers
    ]
    if len(follower_data) == 0:
        return None
    query = """
        INSERT INTO channel_followers (channel_id, fid, followed_at, updated_at)
        VALUES %s
        ON CONFLICT (channel_id, fid) DO UPDATE SET
            followed_at = EXCLUDED.followed_at,
            updated_at = EXCLUDED.updated_at
    """
    execute_db_query(query, follower_data)
    logging.info(f"Stored followers for channel: {channel_id}")


def fetch_followers_for_all_channels(channel_ids):
    total_channels = len(channel_ids)
    logging.info(f"Starting to fetch followers for {total_channels} channels.")

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        # Create a session with retries
        session = create_session_with_retries()

        # Map channels to fetch_and_store_followers with the session
        futures = {
            executor.submit(fetch_and_store_followers, session, channel_id): channel_id
            for channel_id in channel_ids
        }
        # Track progress
        for i, future in enumerate(futures, 1):
            channel_id = futures[future]
            try:
                future.result()  # Wait for the task to complete
                logging.info(f"Processed channel: {channel_id} ({i}/{total_channels})")
            except Exception as e:
                logging.error(f"Error processing channel {channel_id}: {e}")


def main():
    logging.info("Script started.")
    create_tables()
    potential_channel_ids = fetch_and_store_channels(False)
    candidate_channel_ids = []
    for id in potential_channel_ids:
        if id in pocessed_channel_ids:
            continue
        candidate_channel_ids.append(id)
    fetch_followers_for_all_channels(candidate_channel_ids)
    logging.info("Script completed successfully.")


if __name__ == "__main__":
    # Example usage

    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        with conn.cursor() as cur:
            cur.execute("select channel_id from channel_followers group by channel_id")
            results = cur.fetchall()
            # print(result)
    pocessed_channel_ids = set([result[0] for result in results])
    print(pocessed_channel_ids)
    # execute_db_query
    # print("Extracted Channel IDs:", pocessed_channel_ids)
    main()
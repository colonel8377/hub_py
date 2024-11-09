import asyncio
import concurrent.futures
import asyncpg

from typing import List, Tuple
from src.hub_py.generated import request_response_pb2
from src.hub_py.generated.message_pb2 import MessageType
from utils import get_env_client

client = get_env_client(use_async=True)

# Asynchronous function to fetch a batch of fids from the database
async def fetch_fids_batch(pool, batch_size=1000, offset=0) -> List[int]:
    async with pool.acquire() as conn:
        batch = await conn.fetch(f"SELECT fid FROM fids LIMIT {batch_size} OFFSET {offset}")
        return [record['fid'] for record in batch] if batch else []


async def fetch_verification(fids: List) -> List:
    insert_datas = []
    for fid in fids:
        request = request_response_pb2.FidRequest(fid=fid)
        messages_response = client.GetVerificationsByFid(request)
        for msg in messages_response.messages:
            if msg.data and msg.data.type == MessageType.MESSAGE_TYPE_VERIFICATION_ADD_ETH_ADDRESS:
                data = msg.data
                body = data.verification_add_address_body
                insert_datas.append((data.fid, data.network, data.timestamp,
                                     body.address.hex(), body.claim_signature.hex(), body.block_hash.hex()))
    return insert_datas

# Asynchronous function to insert verification data into the database
async def insert_verification_data(pool, data: List[Tuple[int, int, int, str, str, str]]):
    async with pool.acquire() as conn:
        upsert_query = """
        INSERT INTO verification (fid, network, timestamp, address, claim_signature, block_hash, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (fid, address) 
        DO UPDATE SET
            network = EXCLUDED.network,
            timestamp = EXCLUDED.timestamp,
            claim_signature = EXCLUDED.claim_signature,
            block_hash = EXCLUDED.block_hash
            updated_at = CURRENT_TIMESTAMP  -- Update the timestamp on conflict
        """
        await conn.executemany(upsert_query, data)


# Main function to manage fetching and insertion in parallel
async def main(num_workers=8, batch_size=100):
    # Connect to the PostgreSQL database using a connection pool
    pool = await asyncpg.create_pool(
        bname="",
        user="",
        password="",
        host="",
        port=""
    )
    offset = 0
    try:
        # Create a thread pool for fetching verification data
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            while True:
                async with pool.acquire() as conn:
                    # Fetch a batch of fids from the database
                    fids_batch = await conn.fetch(f"SELECT fid FROM fids LIMIT {batch_size} OFFSET {offset}")
                    fids_batch = [record['fid'] for record in fids_batch]
                    if not fids_batch:
                        break  # Exit if no more fids to process

                # Step 1: Fetch verification data concurrently for each fid in the batch
                verification_data_futures = [
                    asyncio.get_running_loop().run_in_executor(executor, fetch_verification, [fid])
                    for fid in fids_batch
                ]
                # Gather all verification data for the batch
                verification_data_batches = await asyncio.gather(*verification_data_futures)

                # Flatten the list of lists into a single list of tuples
                flattened_data = [item for sublist in verification_data_batches for item in sublist]

                # Step 2: Insert the verification data concurrently
                if flattened_data:
                    await insert_verification_data(pool, flattened_data)

                # Move to the next batch
                offset += batch_size
    finally:
        await pool.close()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())


import asyncio
import asyncpg

from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from src.examples.utils import get_env_client
from src.hub_py.generated import request_response_pb2
from src.hub_py.generated.message_pb2 import MessageType


# Asynchronous function to fetch a batch of fids from the database
async def fetch_fids_batch(pool, batch_size=1000, offset=0) -> List[int]:
    async with pool.acquire() as conn:
        batch = await conn.fetch(f"SELECT fid FROM fids LIMIT {batch_size} OFFSET {offset}")
        return [record['fid'] for record in batch] if batch else []


def fetch_verification(fid: int) -> List[Tuple[int, int, int, str, str, str]]:
    client = get_env_client(use_async=False)
    insert_datas = []
    request = request_response_pb2.FidRequest(fid=fid)
    msg_resp = client.GetVerificationsByFid(request)
    for msg in msg_resp.messages:
        if msg.data and msg.data.type == MessageType.MESSAGE_TYPE_VERIFICATION_ADD_ETH_ADDRESS:
            data = msg.data
            body = data.verification_add_address_body
            insert_datas.append((
                int(data.fid),
                int(data.network),
                int(data.timestamp),
                str(body.address.hex()),
                str(body.claim_signature.hex()),
                str(body.block_hash.hex())
            ))
    return insert_datas


# Asynchronous function to insert verification data into the database
async def insert_verification_data(pool, data: List[Tuple[int, int, int, str, str, str]]):
    if not data:
        return

    async with pool.acquire() as conn:
        try:
            upsert_query = """
            INSERT INTO verifications (fid, network, timestamp, address, claim_signature, block_hash, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT (fid, address) 
            DO UPDATE SET
                network = EXCLUDED.network,
                timestamp = EXCLUDED.timestamp,
                claim_signature = EXCLUDED.claim_signature,
                block_hash = EXCLUDED.block_hash,
                updated_at = CURRENT_TIMESTAMP  -- Update the timestamp on conflict
            """
            await conn.executemany(upsert_query, data)
        except Exception as e:
            print(upsert_query)
            print(e)


# Main function to manage fetching and insertion in parallel
async def main(batch_size=10000, max_workers=100):
    pool = await asyncpg.create_pool(
        database="DappResearch",
        user="DappResearch",
        password="FarcasterIndexer",
        host="10.7.127.0",
        port="6541"
    )

    offset = 0
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                fids_batch = await fetch_fids_batch(pool, batch_size, offset)
                if not fids_batch:
                    break  # Exit if no more fids to process

                # Fetch verification data concurrently using threads
                loop = asyncio.get_event_loop()
                verification_data_batches = await asyncio.gather(
                    *[loop.run_in_executor(executor, fetch_verification, fid) for fid in fids_batch]
                )

                # Flatten the list of lists into a single list of tuples
                flattened_data = [item for sublist in verification_data_batches for item in sublist]

                # Insert the verification data if there's any
                await insert_verification_data(pool, flattened_data)

                # Move to the next batch
                offset += batch_size
                if offset % 100000 == 0:
                    print(f'Offset {offset} is finished')
    except Exception as e:
        print(e)
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())

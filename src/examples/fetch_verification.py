import asyncio
import os

import asyncpg
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from src.examples.utils import get_env_client
from src.hub_py.generated import request_response_pb2
from src.hub_py.generated.message_pb2 import MessageType, FarcasterNetwork


async def fetch_fids_batch(pool, batch_size: int = 1000, offset: int = 0) -> List[int]:
    """
    Fetch a batch of FIDs from the database.

    Args:
        pool: The asyncpg connection pool.
        batch_size: Number of FIDs to fetch in each batch.
        offset: Offset for the current batch query.

    Returns:
        A list of FIDs.
    """
    query = "SELECT fid FROM fids LIMIT $1 OFFSET $2"
    async with pool.acquire() as conn:
        try:
            records = await conn.fetch(query, batch_size, offset)
            return [record["fid"] for record in records]
        except Exception as e:
            print(f"Error fetching FIDs at offset {offset}: {e}")
            return []


def fetch_verification(fid: int) -> List[Tuple[int, int, int, bytes, bytes, bytes, int]]:
    """
    Fetch verification data for a single FID.

    Args:
        fid: The FID to fetch verification data for.

    Returns:
        A list of tuples containing verification data.
    """
    client = get_env_client(use_async=False)
    verifications = []
    request = request_response_pb2.FidRequest(fid=fid)

    try:
        msg_resp = client.GetUserDataByFid(request)
        for msg in msg_resp.messages:
            if not msg.data:
                continue
            body = msg.data.verification_add_address_body
            if (
                    msg.data.type == MessageType.MESSAGE_TYPE_VERIFICATION_ADD_ETH_ADDRESS
                    and msg.data.network == FarcasterNetwork.FARCASTER_NETWORK_MAINNET
            ):
                verifications.append(
                    (
                        fid,
                        int(msg.data.network),
                        int(msg.data.timestamp),
                        bytes.fromhex(body.address.hex()),
                        bytes.fromhex(body.claim_signature.hex()),
                        bytes.fromhex(body.block_hash.hex()),
                        int(body.protocol),
                    )
                )
    except Exception as e:
        print(f"Error fetching verification for FID {fid}: {e}")
    return verifications


async def insert_verification_data(
        pool, data: List[Tuple[int, int, int, bytes, bytes, bytes, int]]
):
    """
    Insert verification data into the database.

    Args:
        pool: The asyncpg connection pool.
        data: The verification data to insert.
    """
    if not data:
        return

    query = """
        INSERT INTO user_verification_history (
            fid, 
            network, 
            timestamp, 
            address, 
            claim_signature, 
            block_hash, 
            protocol,
            created_at, 
            updated_at
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (fid, address)
        DO UPDATE SET
            network = EXCLUDED.network,
            timestamp = EXCLUDED.timestamp,
            claim_signature = EXCLUDED.claim_signature,
            block_hash = EXCLUDED.block_hash,
            protocol = EXCLUDED.protocol,
            updated_at = CURRENT_TIMESTAMP;
    """

    async with pool.acquire() as conn:
        try:
            await conn.executemany(query, data)
        except Exception as e:
            print(f"Error inserting verification data: {e}")


async def main(batch_size: int = 10000, max_workers: int = os.cpu_count() * 5):
    """
    Main function to orchestrate fetching and inserting verification data.

    Args:
        batch_size: Number of FIDs to process per batch.
        max_workers: Maximum number of concurrent threads.
    """
    pool = await asyncpg.create_pool(
        database="DappResearch",
        user="DappResearch",
        password="FarcasterIndexer",
        host="100.64.197.124",
        port="6541",
        max_size=max_workers,
    )

    offset = 0
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                fids_batch = await fetch_fids_batch(pool, batch_size, offset)
                if not fids_batch:
                    print("No more FIDs to process. Exiting.")
                    break

                # Fetch verification data concurrently
                loop = asyncio.get_event_loop()
                verification_data_batches = await asyncio.gather(
                    *[loop.run_in_executor(executor, fetch_verification, fid) for fid in fids_batch]
                )

                # Flatten and insert verification data
                flattened_data = [item for batch in verification_data_batches for item in batch]
                await insert_verification_data(pool, flattened_data)

                offset += batch_size
                print(f"Processed {offset} records.")
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
    # print(fetch_verification(862653))
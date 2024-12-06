import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.examples.utils import get_env_client
from src.hub_py.generated.request_response_pb2 import FidRequest, TrieNodePrefix


# Function to fetch username by fid using gRPC
def fetch_sync_tries(bytes, count = 0):
    try:
        client = get_env_client(use_async=False)
        request = TrieNodePrefix(prefix = bytes)
        msg_resp = client.GetSyncMetadataByPrefix(request)
        print(f'Layer: {count} - Prefix: {msg_resp.prefix.hex()} - Msg No: {msg_resp.num_messages}')
        count += 1
        for child in msg_resp.children:
            fetch_sync_tries(child.prefix, count)
    except Exception as e:
        print(f"Failed to fetch tries: {e}")

# Main script
if __name__ == "__main__":
    print(fetch_sync_tries(None, 0))
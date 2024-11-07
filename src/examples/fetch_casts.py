from unicodedata import category

from src.hub_py.builders import make_cast_add, make_cast_delete
from src.hub_py.generated.message_pb2 import CastRemoveBody, MessageData, MessageType
from utils import get_env_client, get_env_fid, get_env_network, get_env_signer

from src.hub_py.generated import request_response_pb2


def main() -> None:
    client = get_env_client()
    fid = get_env_fid()
    network = get_env_network()
    message_data = MessageData(
        fid=fid,
        network=network,
    )
    request = request_response_pb2.FidRequest(fid=fid)
    messages_response = client.GetCastsByFid(request)
    for msg in messages_response.messages:
        print(msg)


if __name__ == "__main__":
    main()

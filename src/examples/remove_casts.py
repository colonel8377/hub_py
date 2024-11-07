from src.examples.utils import covert_farcaster_timestamp
from src.hub_py.builders import make_cast_delete
from src.hub_py.generated import request_response_pb2
from src.hub_py.generated.message_pb2 import CastRemoveBody, MessageData, MessageType
from utils import get_env_client, get_env_fid, get_env_network, get_env_signer


def main() -> None:
    client = get_env_client()
    fid = get_env_fid()
    network = get_env_network()
    message_data = MessageData(
        fid=fid,
        network=network,
        timestamp=covert_farcaster_timestamp(),
    )
    request = request_response_pb2.FidRequest(fid=fid)
    messages_response = client.GetAllCastMessagesByFid(request)
    messages = messages_response.messages
    signer = get_env_signer()
    for msg in messages:
        try:
            if msg.data.type == MessageType.MESSAGE_TYPE_CAST_ADD:
                cast = CastRemoveBody(target_hash=msg.hash)
                submit_msg = make_cast_delete(
                    message_data,
                    signer,
                    cast,
                )
                with open('./submit_msg', "wb") as f:
                    f.write(submit_msg.SerializeToString())
                client.SubmitMessage(submit_msg)
        except Exception as e:
            print(msg, e)


if __name__ == "__main__":
    main()

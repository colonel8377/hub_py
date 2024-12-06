import grpc

from src.hub_py.builders import make_cast_add
from src.hub_py.generated.message_pb2 import (
    MessageData,
    CastAddBody, Embed,
)
from utils import get_env_signer, get_env_fid, get_env_client, get_env_network, covert_farcaster_timestamp


def main() -> None:
    client = get_env_client()
    message_data = MessageData(
        fid=get_env_fid(),
        network=get_env_network(),
        timestamp=covert_farcaster_timestamp(),
    )
    signer = get_env_signer()
    casts = [
        # Example 1: A cast with no mentions
        CastAddBody(
            text="2.This is a cast with no mentions",
            embeds=[],
            mentions=[],
            mentions_positions=[],
        ),
        # Example 2: A cast with mentions
        CastAddBody(
            text=" 2.and  are big fans of ",
            embeds=[],
            mentions=[3, 2, 1],
            mentions_positions=[0, 5, 22],
        ),
        # Example 3: A cast with mentions and an attachment
        CastAddBody(
            text="2.Hey , check this out!",
            embeds=[Embed(url="https://farcaster.xyz")],
            mentions=[3],
            mentions_positions=[4],
        ),
        # Example 4: A cast with mentions and an attachment, and a link in the text
        CastAddBody(
            text="2.Hey , check out https://farcaster.xyz!",
            embeds=[Embed(url="https://farcaster.xyz")],
            mentions=[3],
            mentions_positions=[4],
        ),
        # Example 5: A cast with multiple mentions
        CastAddBody(
            text="2.You can mention  multiple times:   ",
            embeds=[],
            mentions=[2, 2, 2, 2],
            mentions_positions=[16, 33, 34, 35],
        ),
        # Example 6: A cast with emoji and mentions
        CastAddBody(
            text="2.🤓 can mention immediately after emoji",
            embeds=[],
            mentions=[1],
            mentions_positions=[4],
        ),
        # Example 7: A cast with emoji and a link in the text and an attachment
        CastAddBody(
            text="2.🤓https://url-after-unicode.com can include URL immediately after emoji!!s",
            embeds=[Embed(url="https://url-after-unicode.com")],
            mentions=[],
            mentions_positions=[],
        ),
    ]

    for cast in casts:
        try:
            submit_msg = make_cast_add(
                    message_data,
                    signer,
                    cast,
            )
            result = client.SubmitMessage(
                submit_msg
            )
            print(result.data.cast_add_body)
        except grpc.RpcError as e:
            print(e)


if __name__ == "__main__":
    main()

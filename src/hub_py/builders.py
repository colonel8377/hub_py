from blake3 import blake3

from src.hub_py.generated.onchain_event_pb2 import SignerEventBody
from src.hub_py.time import get_farcaster_time
from src.hub_py.signers import Signer, Ed25519Signer
from src.hub_py.generated.message_pb2 import (
    Message,
    MessageData,
    HashScheme,
    MessageType,
    # SignerAddBody,
    UserDataBody,
    CastAddBody,
)
from src.hub_py.protobuf_patch import patched_serialize_to_string


def _make_message(data: MessageData, signer: Signer) -> Message:
    # Set the timestamp if it's not provided
    if data.timestamp is None:
        data.timestamp = get_farcaster_time()
    # TODO: Remove patch and use data.SerializeToString()
    data_bytes = patched_serialize_to_string(data)
    hash = blake3(data_bytes).digest(length=20)
    return Message(
        data=data,
        hash=hash,
        hash_scheme=HashScheme.HASH_SCHEME_BLAKE3,
        signature=signer.sign_hash(hash),
        signature_scheme=signer.signature_scheme(),
        signer=signer.public_key(),
    )


def make_user_data_add(
    data: MessageData, signer: Signer, user_data: UserDataBody
) -> Message:
    # Create a new MessageData object and copy the provided data
    message_data = MessageData()
    message_data.CopyFrom(data)
    message_data.type = MessageType.MESSAGE_TYPE_USER_DATA_ADD
    message_data.user_data_body.CopyFrom(user_data)
    return _make_message(
        message_data,
        signer,
    )


def make_cast_add(data: MessageData, signer: Signer, cast_add: CastAddBody) -> Message:
    # Create a new MessageData object and copy the provided data
    message_data = MessageData()
    message_data.CopyFrom(data)
    message_data.type = MessageType.MESSAGE_TYPE_CAST_ADD
    message_data.cast_add_body.CopyFrom(cast_add)
    return _make_message(
        message_data,
        signer,
    )
import message_pb2 as _message_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
GOSSIP_VERSION_V1: GossipVersion
GOSSIP_VERSION_V1_1: GossipVersion

class AckMessageBody(_message.Message):
    __slots__ = ["ack_origin_peer_id", "ack_timestamp", "ping_origin_peer_id", "ping_timestamp"]
    ACK_ORIGIN_PEER_ID_FIELD_NUMBER: _ClassVar[int]
    ACK_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PING_ORIGIN_PEER_ID_FIELD_NUMBER: _ClassVar[int]
    PING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ack_origin_peer_id: bytes
    ack_timestamp: int
    ping_origin_peer_id: bytes
    ping_timestamp: int
    def __init__(self, ping_origin_peer_id: _Optional[bytes] = ..., ack_origin_peer_id: _Optional[bytes] = ..., ping_timestamp: _Optional[int] = ..., ack_timestamp: _Optional[int] = ...) -> None: ...

class ContactInfoContent(_message.Message):
    __slots__ = ["app_version", "body", "count", "data_bytes", "excluded_hashes", "gossip_address", "hub_version", "network", "rpc_address", "signature", "signer", "timestamp"]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_BYTES_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_HASHES_FIELD_NUMBER: _ClassVar[int]
    GOSSIP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    HUB_VERSION_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    RPC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    app_version: str
    body: ContactInfoContentBody
    count: int
    data_bytes: bytes
    excluded_hashes: _containers.RepeatedScalarFieldContainer[str]
    gossip_address: GossipAddressInfo
    hub_version: str
    network: _message_pb2.FarcasterNetwork
    rpc_address: GossipAddressInfo
    signature: bytes
    signer: bytes
    timestamp: int
    def __init__(self, gossip_address: _Optional[_Union[GossipAddressInfo, _Mapping]] = ..., rpc_address: _Optional[_Union[GossipAddressInfo, _Mapping]] = ..., excluded_hashes: _Optional[_Iterable[str]] = ..., count: _Optional[int] = ..., hub_version: _Optional[str] = ..., network: _Optional[_Union[_message_pb2.FarcasterNetwork, str]] = ..., app_version: _Optional[str] = ..., timestamp: _Optional[int] = ..., body: _Optional[_Union[ContactInfoContentBody, _Mapping]] = ..., signature: _Optional[bytes] = ..., signer: _Optional[bytes] = ..., data_bytes: _Optional[bytes] = ...) -> None: ...

class ContactInfoContentBody(_message.Message):
    __slots__ = ["app_version", "count", "excluded_hashes", "gossip_address", "hub_version", "network", "rpc_address", "timestamp"]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_HASHES_FIELD_NUMBER: _ClassVar[int]
    GOSSIP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    HUB_VERSION_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    RPC_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    app_version: str
    count: int
    excluded_hashes: _containers.RepeatedScalarFieldContainer[str]
    gossip_address: GossipAddressInfo
    hub_version: str
    network: _message_pb2.FarcasterNetwork
    rpc_address: GossipAddressInfo
    timestamp: int
    def __init__(self, gossip_address: _Optional[_Union[GossipAddressInfo, _Mapping]] = ..., rpc_address: _Optional[_Union[GossipAddressInfo, _Mapping]] = ..., excluded_hashes: _Optional[_Iterable[str]] = ..., count: _Optional[int] = ..., hub_version: _Optional[str] = ..., network: _Optional[_Union[_message_pb2.FarcasterNetwork, str]] = ..., app_version: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class GossipAddressInfo(_message.Message):
    __slots__ = ["address", "dns_name", "family", "port"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    DNS_NAME_FIELD_NUMBER: _ClassVar[int]
    FAMILY_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    address: str
    dns_name: str
    family: int
    port: int
    def __init__(self, address: _Optional[str] = ..., family: _Optional[int] = ..., port: _Optional[int] = ..., dns_name: _Optional[str] = ...) -> None: ...

class GossipMessage(_message.Message):
    __slots__ = ["contact_info_content", "message", "message_bundle", "network_latency_message", "peer_id", "timestamp", "topics", "version"]
    CONTACT_INFO_CONTENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BUNDLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NETWORK_LATENCY_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PEER_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    contact_info_content: ContactInfoContent
    message: _message_pb2.Message
    message_bundle: MessageBundle
    network_latency_message: NetworkLatencyMessage
    peer_id: bytes
    timestamp: int
    topics: _containers.RepeatedScalarFieldContainer[str]
    version: GossipVersion
    def __init__(self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ..., contact_info_content: _Optional[_Union[ContactInfoContent, _Mapping]] = ..., network_latency_message: _Optional[_Union[NetworkLatencyMessage, _Mapping]] = ..., message_bundle: _Optional[_Union[MessageBundle, _Mapping]] = ..., topics: _Optional[_Iterable[str]] = ..., peer_id: _Optional[bytes] = ..., version: _Optional[_Union[GossipVersion, str]] = ..., timestamp: _Optional[int] = ...) -> None: ...

class MessageBundle(_message.Message):
    __slots__ = ["hash", "messages"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    hash: bytes
    messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    def __init__(self, hash: _Optional[bytes] = ..., messages: _Optional[_Iterable[_Union[_message_pb2.Message, _Mapping]]] = ...) -> None: ...

class NetworkLatencyMessage(_message.Message):
    __slots__ = ["ack_message", "ping_message"]
    ACK_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PING_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ack_message: AckMessageBody
    ping_message: PingMessageBody
    def __init__(self, ping_message: _Optional[_Union[PingMessageBody, _Mapping]] = ..., ack_message: _Optional[_Union[AckMessageBody, _Mapping]] = ...) -> None: ...

class PingMessageBody(_message.Message):
    __slots__ = ["ping_origin_peer_id", "ping_timestamp"]
    PING_ORIGIN_PEER_ID_FIELD_NUMBER: _ClassVar[int]
    PING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ping_origin_peer_id: bytes
    ping_timestamp: int
    def __init__(self, ping_origin_peer_id: _Optional[bytes] = ..., ping_timestamp: _Optional[int] = ...) -> None: ...

class GossipVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

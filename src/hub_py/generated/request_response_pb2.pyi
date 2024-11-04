import message_pb2 as _message_pb2
import onchain_event_pb2 as _onchain_event_pb2
import hub_event_pb2 as _hub_event_pb2
import username_proof_pb2 as _username_proof_pb2
import gossip_pb2 as _gossip_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
STORE_TYPE_CASTS: StoreType
STORE_TYPE_LINKS: StoreType
STORE_TYPE_NONE: StoreType
STORE_TYPE_REACTIONS: StoreType
STORE_TYPE_USERNAME_PROOFS: StoreType
STORE_TYPE_USER_DATA: StoreType
STORE_TYPE_VERIFICATIONS: StoreType
UNIT_TYPE_2024: StorageUnitType
UNIT_TYPE_LEGACY: StorageUnitType

class BulkMessageResponse(_message.Message):
    __slots__ = ["message", "message_error"]
    MESSAGE_ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    message_error: MessageError
    def __init__(self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ..., message_error: _Optional[_Union[MessageError, _Mapping]] = ...) -> None: ...

class CastsByParentRequest(_message.Message):
    __slots__ = ["page_size", "page_token", "parent_cast_id", "parent_url", "reverse"]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PARENT_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_URL_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: bytes
    parent_cast_id: _message_pb2.CastId
    parent_url: str
    reverse: bool
    def __init__(self, parent_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ..., parent_url: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class ContactInfoResponse(_message.Message):
    __slots__ = ["contacts"]
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    contacts: _containers.RepeatedCompositeFieldContainer[_gossip_pb2.ContactInfoContentBody]
    def __init__(self, contacts: _Optional[_Iterable[_Union[_gossip_pb2.ContactInfoContentBody, _Mapping]]] = ...) -> None: ...

class DbStats(_message.Message):
    __slots__ = ["approx_size", "num_fid_events", "num_fname_events", "num_messages"]
    APPROX_SIZE_FIELD_NUMBER: _ClassVar[int]
    NUM_FID_EVENTS_FIELD_NUMBER: _ClassVar[int]
    NUM_FNAME_EVENTS_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    approx_size: int
    num_fid_events: int
    num_fname_events: int
    num_messages: int
    def __init__(self, num_messages: _Optional[int] = ..., num_fid_events: _Optional[int] = ..., num_fname_events: _Optional[int] = ..., approx_size: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EventRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class FidRequest(_message.Message):
    __slots__ = ["fid", "page_size", "page_token", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(self, fid: _Optional[int] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class FidTimestampRequest(_message.Message):
    __slots__ = ["fid", "page_size", "page_token", "reverse", "start_timestamp", "stop_timestamp"]
    FID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STOP_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    fid: int
    page_size: int
    page_token: bytes
    reverse: bool
    start_timestamp: int
    stop_timestamp: int
    def __init__(self, fid: _Optional[int] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ..., start_timestamp: _Optional[int] = ..., stop_timestamp: _Optional[int] = ...) -> None: ...

class FidsRequest(_message.Message):
    __slots__ = ["page_size", "page_token", "reverse"]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class FidsResponse(_message.Message):
    __slots__ = ["fids", "next_page_token"]
    FIDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    fids: _containers.RepeatedScalarFieldContainer[int]
    next_page_token: bytes
    def __init__(self, fids: _Optional[_Iterable[int]] = ..., next_page_token: _Optional[bytes] = ...) -> None: ...

class HubInfoRequest(_message.Message):
    __slots__ = ["db_stats"]
    DB_STATS_FIELD_NUMBER: _ClassVar[int]
    db_stats: bool
    def __init__(self, db_stats: bool = ...) -> None: ...

class HubInfoResponse(_message.Message):
    __slots__ = ["db_stats", "hub_operator_fid", "is_syncing", "nickname", "peerId", "root_hash", "version"]
    DB_STATS_FIELD_NUMBER: _ClassVar[int]
    HUB_OPERATOR_FID_FIELD_NUMBER: _ClassVar[int]
    IS_SYNCING_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    ROOT_HASH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    db_stats: DbStats
    hub_operator_fid: int
    is_syncing: bool
    nickname: str
    peerId: str
    root_hash: str
    version: str
    def __init__(self, version: _Optional[str] = ..., is_syncing: bool = ..., nickname: _Optional[str] = ..., root_hash: _Optional[str] = ..., db_stats: _Optional[_Union[DbStats, _Mapping]] = ..., peerId: _Optional[str] = ..., hub_operator_fid: _Optional[int] = ...) -> None: ...

class IdRegistryEventByAddressRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    def __init__(self, address: _Optional[bytes] = ...) -> None: ...

class LinkRequest(_message.Message):
    __slots__ = ["fid", "link_type", "target_fid"]
    FID_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FID_FIELD_NUMBER: _ClassVar[int]
    fid: int
    link_type: str
    target_fid: int
    def __init__(self, fid: _Optional[int] = ..., link_type: _Optional[str] = ..., target_fid: _Optional[int] = ...) -> None: ...

class LinksByFidRequest(_message.Message):
    __slots__ = ["fid", "link_type", "page_size", "page_token", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    link_type: str
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(self, fid: _Optional[int] = ..., link_type: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class LinksByTargetRequest(_message.Message):
    __slots__ = ["link_type", "page_size", "page_token", "reverse", "target_fid"]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FID_FIELD_NUMBER: _ClassVar[int]
    link_type: str
    page_size: int
    page_token: bytes
    reverse: bool
    target_fid: int
    def __init__(self, target_fid: _Optional[int] = ..., link_type: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class MessageError(_message.Message):
    __slots__ = ["errCode", "hash", "message"]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    errCode: str
    hash: bytes
    message: str
    def __init__(self, hash: _Optional[bytes] = ..., errCode: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MessagesResponse(_message.Message):
    __slots__ = ["messages", "next_page_token"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    next_page_token: bytes
    def __init__(self, messages: _Optional[_Iterable[_Union[_message_pb2.Message, _Mapping]]] = ..., next_page_token: _Optional[bytes] = ...) -> None: ...

class NameRegistryEventRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: bytes
    def __init__(self, name: _Optional[bytes] = ...) -> None: ...

class OnChainEventRequest(_message.Message):
    __slots__ = ["event_type", "fid", "page_size", "page_token", "reverse"]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    event_type: _onchain_event_pb2.OnChainEventType
    fid: int
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(self, fid: _Optional[int] = ..., event_type: _Optional[_Union[_onchain_event_pb2.OnChainEventType, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class OnChainEventResponse(_message.Message):
    __slots__ = ["events", "next_page_token"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_onchain_event_pb2.OnChainEvent]
    next_page_token: bytes
    def __init__(self, events: _Optional[_Iterable[_Union[_onchain_event_pb2.OnChainEvent, _Mapping]]] = ..., next_page_token: _Optional[bytes] = ...) -> None: ...

class ReactionRequest(_message.Message):
    __slots__ = ["fid", "reaction_type", "target_cast_id", "target_url"]
    FID_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_URL_FIELD_NUMBER: _ClassVar[int]
    fid: int
    reaction_type: _message_pb2.ReactionType
    target_cast_id: _message_pb2.CastId
    target_url: str
    def __init__(self, fid: _Optional[int] = ..., reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ..., target_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ..., target_url: _Optional[str] = ...) -> None: ...

class ReactionsByFidRequest(_message.Message):
    __slots__ = ["fid", "page_size", "page_token", "reaction_type", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    page_size: int
    page_token: bytes
    reaction_type: _message_pb2.ReactionType
    reverse: bool
    def __init__(self, fid: _Optional[int] = ..., reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class ReactionsByTargetRequest(_message.Message):
    __slots__ = ["page_size", "page_token", "reaction_type", "reverse", "target_cast_id", "target_url"]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    TARGET_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_URL_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: bytes
    reaction_type: _message_pb2.ReactionType
    reverse: bool
    target_cast_id: _message_pb2.CastId
    target_url: str
    def __init__(self, target_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ..., target_url: _Optional[str] = ..., reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ..., page_size: _Optional[int] = ..., page_token: _Optional[bytes] = ..., reverse: bool = ...) -> None: ...

class RentRegistryEventsRequest(_message.Message):
    __slots__ = ["fid"]
    FID_FIELD_NUMBER: _ClassVar[int]
    fid: int
    def __init__(self, fid: _Optional[int] = ...) -> None: ...

class SignerRequest(_message.Message):
    __slots__ = ["fid", "signer"]
    FID_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    fid: int
    signer: bytes
    def __init__(self, fid: _Optional[int] = ..., signer: _Optional[bytes] = ...) -> None: ...

class StorageLimit(_message.Message):
    __slots__ = ["earliestHash", "earliestTimestamp", "limit", "name", "store_type", "used"]
    EARLIESTHASH_FIELD_NUMBER: _ClassVar[int]
    EARLIESTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USED_FIELD_NUMBER: _ClassVar[int]
    earliestHash: bytes
    earliestTimestamp: int
    limit: int
    name: str
    store_type: StoreType
    used: int
    def __init__(self, store_type: _Optional[_Union[StoreType, str]] = ..., name: _Optional[str] = ..., limit: _Optional[int] = ..., used: _Optional[int] = ..., earliestTimestamp: _Optional[int] = ..., earliestHash: _Optional[bytes] = ...) -> None: ...

class StorageLimitsResponse(_message.Message):
    __slots__ = ["limits", "unit_details", "units"]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    UNIT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    limits: _containers.RepeatedCompositeFieldContainer[StorageLimit]
    unit_details: _containers.RepeatedCompositeFieldContainer[StorageUnitDetails]
    units: int
    def __init__(self, limits: _Optional[_Iterable[_Union[StorageLimit, _Mapping]]] = ..., units: _Optional[int] = ..., unit_details: _Optional[_Iterable[_Union[StorageUnitDetails, _Mapping]]] = ...) -> None: ...

class StorageUnitDetails(_message.Message):
    __slots__ = ["unit_size", "unit_type"]
    UNIT_SIZE_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    unit_size: int
    unit_type: StorageUnitType
    def __init__(self, unit_type: _Optional[_Union[StorageUnitType, str]] = ..., unit_size: _Optional[int] = ...) -> None: ...

class StreamError(_message.Message):
    __slots__ = ["errCode", "message", "request"]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    errCode: str
    message: str
    request: str
    def __init__(self, errCode: _Optional[str] = ..., message: _Optional[str] = ..., request: _Optional[str] = ...) -> None: ...

class StreamFetchRequest(_message.Message):
    __slots__ = ["cast_messages_by_fid", "idempotency_key", "link_messages_by_fid", "reaction_messages_by_fid", "user_data_messages_by_fid", "verification_messages_by_fid"]
    CAST_MESSAGES_BY_FID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    LINK_MESSAGES_BY_FID_FIELD_NUMBER: _ClassVar[int]
    REACTION_MESSAGES_BY_FID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_MESSAGES_BY_FID_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_MESSAGES_BY_FID_FIELD_NUMBER: _ClassVar[int]
    cast_messages_by_fid: FidTimestampRequest
    idempotency_key: str
    link_messages_by_fid: FidTimestampRequest
    reaction_messages_by_fid: FidTimestampRequest
    user_data_messages_by_fid: FidTimestampRequest
    verification_messages_by_fid: FidTimestampRequest
    def __init__(self, idempotency_key: _Optional[str] = ..., cast_messages_by_fid: _Optional[_Union[FidTimestampRequest, _Mapping]] = ..., reaction_messages_by_fid: _Optional[_Union[FidTimestampRequest, _Mapping]] = ..., verification_messages_by_fid: _Optional[_Union[FidTimestampRequest, _Mapping]] = ..., user_data_messages_by_fid: _Optional[_Union[FidTimestampRequest, _Mapping]] = ..., link_messages_by_fid: _Optional[_Union[FidTimestampRequest, _Mapping]] = ...) -> None: ...

class StreamFetchResponse(_message.Message):
    __slots__ = ["error", "idempotency_key", "messages"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    error: StreamError
    idempotency_key: str
    messages: MessagesResponse
    def __init__(self, idempotency_key: _Optional[str] = ..., messages: _Optional[_Union[MessagesResponse, _Mapping]] = ..., error: _Optional[_Union[StreamError, _Mapping]] = ...) -> None: ...

class StreamSyncRequest(_message.Message):
    __slots__ = ["force_sync", "get_all_messages_by_sync_ids", "get_all_sync_ids_by_prefix", "get_current_peers", "get_info", "get_on_chain_events", "get_on_chain_signers_by_fid", "get_sync_metadata_by_prefix", "get_sync_snapshot_by_prefix", "get_sync_status", "stop_sync"]
    FORCE_SYNC_FIELD_NUMBER: _ClassVar[int]
    GET_ALL_MESSAGES_BY_SYNC_IDS_FIELD_NUMBER: _ClassVar[int]
    GET_ALL_SYNC_IDS_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_CURRENT_PEERS_FIELD_NUMBER: _ClassVar[int]
    GET_INFO_FIELD_NUMBER: _ClassVar[int]
    GET_ON_CHAIN_EVENTS_FIELD_NUMBER: _ClassVar[int]
    GET_ON_CHAIN_SIGNERS_BY_FID_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_METADATA_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_SNAPSHOT_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_STATUS_FIELD_NUMBER: _ClassVar[int]
    STOP_SYNC_FIELD_NUMBER: _ClassVar[int]
    force_sync: SyncStatusRequest
    get_all_messages_by_sync_ids: SyncIds
    get_all_sync_ids_by_prefix: TrieNodePrefix
    get_current_peers: Empty
    get_info: HubInfoRequest
    get_on_chain_events: OnChainEventRequest
    get_on_chain_signers_by_fid: FidRequest
    get_sync_metadata_by_prefix: TrieNodePrefix
    get_sync_snapshot_by_prefix: TrieNodePrefix
    get_sync_status: SyncStatusRequest
    stop_sync: Empty
    def __init__(self, get_info: _Optional[_Union[HubInfoRequest, _Mapping]] = ..., get_current_peers: _Optional[_Union[Empty, _Mapping]] = ..., stop_sync: _Optional[_Union[Empty, _Mapping]] = ..., force_sync: _Optional[_Union[SyncStatusRequest, _Mapping]] = ..., get_sync_status: _Optional[_Union[SyncStatusRequest, _Mapping]] = ..., get_all_sync_ids_by_prefix: _Optional[_Union[TrieNodePrefix, _Mapping]] = ..., get_all_messages_by_sync_ids: _Optional[_Union[SyncIds, _Mapping]] = ..., get_sync_metadata_by_prefix: _Optional[_Union[TrieNodePrefix, _Mapping]] = ..., get_sync_snapshot_by_prefix: _Optional[_Union[TrieNodePrefix, _Mapping]] = ..., get_on_chain_events: _Optional[_Union[OnChainEventRequest, _Mapping]] = ..., get_on_chain_signers_by_fid: _Optional[_Union[FidRequest, _Mapping]] = ...) -> None: ...

class StreamSyncResponse(_message.Message):
    __slots__ = ["error", "force_sync", "get_all_messages_by_sync_ids", "get_all_sync_ids_by_prefix", "get_current_peers", "get_info", "get_on_chain_events", "get_on_chain_signers_by_fid", "get_sync_metadata_by_prefix", "get_sync_snapshot_by_prefix", "get_sync_status", "stop_sync"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FORCE_SYNC_FIELD_NUMBER: _ClassVar[int]
    GET_ALL_MESSAGES_BY_SYNC_IDS_FIELD_NUMBER: _ClassVar[int]
    GET_ALL_SYNC_IDS_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_CURRENT_PEERS_FIELD_NUMBER: _ClassVar[int]
    GET_INFO_FIELD_NUMBER: _ClassVar[int]
    GET_ON_CHAIN_EVENTS_FIELD_NUMBER: _ClassVar[int]
    GET_ON_CHAIN_SIGNERS_BY_FID_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_METADATA_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_SNAPSHOT_BY_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GET_SYNC_STATUS_FIELD_NUMBER: _ClassVar[int]
    STOP_SYNC_FIELD_NUMBER: _ClassVar[int]
    error: StreamError
    force_sync: SyncStatusResponse
    get_all_messages_by_sync_ids: MessagesResponse
    get_all_sync_ids_by_prefix: SyncIds
    get_current_peers: ContactInfoResponse
    get_info: HubInfoResponse
    get_on_chain_events: OnChainEventResponse
    get_on_chain_signers_by_fid: OnChainEventResponse
    get_sync_metadata_by_prefix: TrieNodeMetadataResponse
    get_sync_snapshot_by_prefix: TrieNodeSnapshotResponse
    get_sync_status: SyncStatusResponse
    stop_sync: SyncStatusResponse
    def __init__(self, get_info: _Optional[_Union[HubInfoResponse, _Mapping]] = ..., get_current_peers: _Optional[_Union[ContactInfoResponse, _Mapping]] = ..., stop_sync: _Optional[_Union[SyncStatusResponse, _Mapping]] = ..., force_sync: _Optional[_Union[SyncStatusResponse, _Mapping]] = ..., get_sync_status: _Optional[_Union[SyncStatusResponse, _Mapping]] = ..., get_all_sync_ids_by_prefix: _Optional[_Union[SyncIds, _Mapping]] = ..., get_all_messages_by_sync_ids: _Optional[_Union[MessagesResponse, _Mapping]] = ..., get_sync_metadata_by_prefix: _Optional[_Union[TrieNodeMetadataResponse, _Mapping]] = ..., get_sync_snapshot_by_prefix: _Optional[_Union[TrieNodeSnapshotResponse, _Mapping]] = ..., get_on_chain_events: _Optional[_Union[OnChainEventResponse, _Mapping]] = ..., get_on_chain_signers_by_fid: _Optional[_Union[OnChainEventResponse, _Mapping]] = ..., error: _Optional[_Union[StreamError, _Mapping]] = ...) -> None: ...

class SubmitBulkMessagesRequest(_message.Message):
    __slots__ = ["messages"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    def __init__(self, messages: _Optional[_Iterable[_Union[_message_pb2.Message, _Mapping]]] = ...) -> None: ...

class SubmitBulkMessagesResponse(_message.Message):
    __slots__ = ["messages"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[BulkMessageResponse]
    def __init__(self, messages: _Optional[_Iterable[_Union[BulkMessageResponse, _Mapping]]] = ...) -> None: ...

class SubscribeRequest(_message.Message):
    __slots__ = ["event_types", "from_id", "shard_index", "total_shards"]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    FROM_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_INDEX_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SHARDS_FIELD_NUMBER: _ClassVar[int]
    event_types: _containers.RepeatedScalarFieldContainer[_hub_event_pb2.HubEventType]
    from_id: int
    shard_index: int
    total_shards: int
    def __init__(self, event_types: _Optional[_Iterable[_Union[_hub_event_pb2.HubEventType, str]]] = ..., from_id: _Optional[int] = ..., total_shards: _Optional[int] = ..., shard_index: _Optional[int] = ...) -> None: ...

class SyncIds(_message.Message):
    __slots__ = ["sync_ids"]
    SYNC_IDS_FIELD_NUMBER: _ClassVar[int]
    sync_ids: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, sync_ids: _Optional[_Iterable[bytes]] = ...) -> None: ...

class SyncStatus(_message.Message):
    __slots__ = ["divergencePrefix", "divergenceSecondsAgo", "inSync", "lastBadSync", "ourMessages", "peerId", "score", "shouldSync", "theirMessages"]
    DIVERGENCEPREFIX_FIELD_NUMBER: _ClassVar[int]
    DIVERGENCESECONDSAGO_FIELD_NUMBER: _ClassVar[int]
    INSYNC_FIELD_NUMBER: _ClassVar[int]
    LASTBADSYNC_FIELD_NUMBER: _ClassVar[int]
    OURMESSAGES_FIELD_NUMBER: _ClassVar[int]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    SHOULDSYNC_FIELD_NUMBER: _ClassVar[int]
    THEIRMESSAGES_FIELD_NUMBER: _ClassVar[int]
    divergencePrefix: str
    divergenceSecondsAgo: int
    inSync: str
    lastBadSync: int
    ourMessages: int
    peerId: str
    score: int
    shouldSync: bool
    theirMessages: int
    def __init__(self, peerId: _Optional[str] = ..., inSync: _Optional[str] = ..., shouldSync: bool = ..., divergencePrefix: _Optional[str] = ..., divergenceSecondsAgo: _Optional[int] = ..., theirMessages: _Optional[int] = ..., ourMessages: _Optional[int] = ..., lastBadSync: _Optional[int] = ..., score: _Optional[int] = ...) -> None: ...

class SyncStatusRequest(_message.Message):
    __slots__ = ["peerId"]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class SyncStatusResponse(_message.Message):
    __slots__ = ["engine_started", "is_syncing", "sync_status"]
    ENGINE_STARTED_FIELD_NUMBER: _ClassVar[int]
    IS_SYNCING_FIELD_NUMBER: _ClassVar[int]
    SYNC_STATUS_FIELD_NUMBER: _ClassVar[int]
    engine_started: bool
    is_syncing: bool
    sync_status: _containers.RepeatedCompositeFieldContainer[SyncStatus]
    def __init__(self, is_syncing: bool = ..., sync_status: _Optional[_Iterable[_Union[SyncStatus, _Mapping]]] = ..., engine_started: bool = ...) -> None: ...

class TrieNodeMetadataResponse(_message.Message):
    __slots__ = ["children", "hash", "num_messages", "prefix"]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    children: _containers.RepeatedCompositeFieldContainer[TrieNodeMetadataResponse]
    hash: str
    num_messages: int
    prefix: bytes
    def __init__(self, prefix: _Optional[bytes] = ..., num_messages: _Optional[int] = ..., hash: _Optional[str] = ..., children: _Optional[_Iterable[_Union[TrieNodeMetadataResponse, _Mapping]]] = ...) -> None: ...

class TrieNodePrefix(_message.Message):
    __slots__ = ["prefix"]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    def __init__(self, prefix: _Optional[bytes] = ...) -> None: ...

class TrieNodeSnapshotResponse(_message.Message):
    __slots__ = ["excluded_hashes", "num_messages", "prefix", "root_hash"]
    EXCLUDED_HASHES_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    ROOT_HASH_FIELD_NUMBER: _ClassVar[int]
    excluded_hashes: _containers.RepeatedScalarFieldContainer[str]
    num_messages: int
    prefix: bytes
    root_hash: str
    def __init__(self, prefix: _Optional[bytes] = ..., excluded_hashes: _Optional[_Iterable[str]] = ..., num_messages: _Optional[int] = ..., root_hash: _Optional[str] = ...) -> None: ...

class UserDataRequest(_message.Message):
    __slots__ = ["fid", "user_data_type"]
    FID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    user_data_type: _message_pb2.UserDataType
    def __init__(self, fid: _Optional[int] = ..., user_data_type: _Optional[_Union[_message_pb2.UserDataType, str]] = ...) -> None: ...

class UsernameProofRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: bytes
    def __init__(self, name: _Optional[bytes] = ...) -> None: ...

class UsernameProofsResponse(_message.Message):
    __slots__ = ["proofs"]
    PROOFS_FIELD_NUMBER: _ClassVar[int]
    proofs: _containers.RepeatedCompositeFieldContainer[_username_proof_pb2.UserNameProof]
    def __init__(self, proofs: _Optional[_Iterable[_Union[_username_proof_pb2.UserNameProof, _Mapping]]] = ...) -> None: ...

class ValidationResponse(_message.Message):
    __slots__ = ["message", "valid"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    valid: bool
    def __init__(self, valid: bool = ..., message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...) -> None: ...

class VerificationRequest(_message.Message):
    __slots__ = ["address", "fid"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    fid: int
    def __init__(self, fid: _Optional[int] = ..., address: _Optional[bytes] = ...) -> None: ...

class StoreType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StorageUnitType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

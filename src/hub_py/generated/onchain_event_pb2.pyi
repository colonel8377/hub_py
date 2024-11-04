from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
EVENT_TYPE_ID_REGISTER: OnChainEventType
EVENT_TYPE_NONE: OnChainEventType
EVENT_TYPE_SIGNER: OnChainEventType
EVENT_TYPE_SIGNER_MIGRATED: OnChainEventType
EVENT_TYPE_STORAGE_RENT: OnChainEventType
ID_REGISTER_EVENT_TYPE_CHANGE_RECOVERY: IdRegisterEventType
ID_REGISTER_EVENT_TYPE_NONE: IdRegisterEventType
ID_REGISTER_EVENT_TYPE_REGISTER: IdRegisterEventType
ID_REGISTER_EVENT_TYPE_TRANSFER: IdRegisterEventType
SIGNER_EVENT_TYPE_ADD: SignerEventType
SIGNER_EVENT_TYPE_ADMIN_RESET: SignerEventType
SIGNER_EVENT_TYPE_NONE: SignerEventType
SIGNER_EVENT_TYPE_REMOVE: SignerEventType

class IdRegisterEventBody(_message.Message):
    __slots__ = ["event_type", "recovery_address", "to"]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    event_type: IdRegisterEventType
    recovery_address: bytes
    to: bytes
    def __init__(self, to: _Optional[bytes] = ..., event_type: _Optional[_Union[IdRegisterEventType, str]] = ..., recovery_address: _Optional[bytes] = ..., **kwargs) -> None: ...

class OnChainEvent(_message.Message):
    __slots__ = ["block_hash", "block_number", "block_timestamp", "chain_id", "fid", "id_register_event_body", "log_index", "signer_event_body", "signer_migrated_event_body", "storage_rent_event_body", "transaction_hash", "tx_index", "type", "version"]
    BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    BLOCK_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    ID_REGISTER_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    LOG_INDEX_FIELD_NUMBER: _ClassVar[int]
    SIGNER_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    SIGNER_MIGRATED_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    STORAGE_RENT_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    TX_INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    block_hash: bytes
    block_number: int
    block_timestamp: int
    chain_id: int
    fid: int
    id_register_event_body: IdRegisterEventBody
    log_index: int
    signer_event_body: SignerEventBody
    signer_migrated_event_body: SignerMigratedEventBody
    storage_rent_event_body: StorageRentEventBody
    transaction_hash: bytes
    tx_index: int
    type: OnChainEventType
    version: int
    def __init__(self, type: _Optional[_Union[OnChainEventType, str]] = ..., chain_id: _Optional[int] = ..., block_number: _Optional[int] = ..., block_hash: _Optional[bytes] = ..., block_timestamp: _Optional[int] = ..., transaction_hash: _Optional[bytes] = ..., log_index: _Optional[int] = ..., fid: _Optional[int] = ..., signer_event_body: _Optional[_Union[SignerEventBody, _Mapping]] = ..., signer_migrated_event_body: _Optional[_Union[SignerMigratedEventBody, _Mapping]] = ..., id_register_event_body: _Optional[_Union[IdRegisterEventBody, _Mapping]] = ..., storage_rent_event_body: _Optional[_Union[StorageRentEventBody, _Mapping]] = ..., tx_index: _Optional[int] = ..., version: _Optional[int] = ...) -> None: ...

class SignerEventBody(_message.Message):
    __slots__ = ["event_type", "key", "key_type", "metadata", "metadata_type"]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    event_type: SignerEventType
    key: bytes
    key_type: int
    metadata: bytes
    metadata_type: int
    def __init__(self, key: _Optional[bytes] = ..., key_type: _Optional[int] = ..., event_type: _Optional[_Union[SignerEventType, str]] = ..., metadata: _Optional[bytes] = ..., metadata_type: _Optional[int] = ...) -> None: ...

class SignerMigratedEventBody(_message.Message):
    __slots__ = ["migratedAt"]
    MIGRATEDAT_FIELD_NUMBER: _ClassVar[int]
    migratedAt: int
    def __init__(self, migratedAt: _Optional[int] = ...) -> None: ...

class StorageRentEventBody(_message.Message):
    __slots__ = ["expiry", "payer", "units"]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    PAYER_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    expiry: int
    payer: bytes
    units: int
    def __init__(self, payer: _Optional[bytes] = ..., units: _Optional[int] = ..., expiry: _Optional[int] = ...) -> None: ...

class OnChainEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SignerEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class IdRegisterEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

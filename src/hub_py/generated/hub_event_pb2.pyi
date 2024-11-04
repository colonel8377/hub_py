import message_pb2 as _message_pb2
import onchain_event_pb2 as _onchain_event_pb2
import username_proof_pb2 as _username_proof_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
HUB_EVENT_TYPE_MERGE_MESSAGE: HubEventType
HUB_EVENT_TYPE_MERGE_ON_CHAIN_EVENT: HubEventType
HUB_EVENT_TYPE_MERGE_USERNAME_PROOF: HubEventType
HUB_EVENT_TYPE_NONE: HubEventType
HUB_EVENT_TYPE_PRUNE_MESSAGE: HubEventType
HUB_EVENT_TYPE_REVOKE_MESSAGE: HubEventType

class HubEvent(_message.Message):
    __slots__ = ["id", "merge_message_body", "merge_on_chain_event_body", "merge_username_proof_body", "prune_message_body", "revoke_message_body", "type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MERGE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_ON_CHAIN_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_USERNAME_PROOF_BODY_FIELD_NUMBER: _ClassVar[int]
    PRUNE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    REVOKE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    merge_message_body: MergeMessageBody
    merge_on_chain_event_body: MergeOnChainEventBody
    merge_username_proof_body: MergeUserNameProofBody
    prune_message_body: PruneMessageBody
    revoke_message_body: RevokeMessageBody
    type: HubEventType
    def __init__(self, type: _Optional[_Union[HubEventType, str]] = ..., id: _Optional[int] = ..., merge_message_body: _Optional[_Union[MergeMessageBody, _Mapping]] = ..., prune_message_body: _Optional[_Union[PruneMessageBody, _Mapping]] = ..., revoke_message_body: _Optional[_Union[RevokeMessageBody, _Mapping]] = ..., merge_username_proof_body: _Optional[_Union[MergeUserNameProofBody, _Mapping]] = ..., merge_on_chain_event_body: _Optional[_Union[MergeOnChainEventBody, _Mapping]] = ...) -> None: ...

class MergeMessageBody(_message.Message):
    __slots__ = ["deleted_messages", "message"]
    DELETED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    deleted_messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    message: _message_pb2.Message
    def __init__(self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ..., deleted_messages: _Optional[_Iterable[_Union[_message_pb2.Message, _Mapping]]] = ...) -> None: ...

class MergeOnChainEventBody(_message.Message):
    __slots__ = ["on_chain_event"]
    ON_CHAIN_EVENT_FIELD_NUMBER: _ClassVar[int]
    on_chain_event: _onchain_event_pb2.OnChainEvent
    def __init__(self, on_chain_event: _Optional[_Union[_onchain_event_pb2.OnChainEvent, _Mapping]] = ...) -> None: ...

class MergeUserNameProofBody(_message.Message):
    __slots__ = ["deleted_username_proof", "deleted_username_proof_message", "username_proof", "username_proof_message"]
    DELETED_USERNAME_PROOF_FIELD_NUMBER: _ClassVar[int]
    DELETED_USERNAME_PROOF_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_PROOF_FIELD_NUMBER: _ClassVar[int]
    USERNAME_PROOF_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    deleted_username_proof: _username_proof_pb2.UserNameProof
    deleted_username_proof_message: _message_pb2.Message
    username_proof: _username_proof_pb2.UserNameProof
    username_proof_message: _message_pb2.Message
    def __init__(self, username_proof: _Optional[_Union[_username_proof_pb2.UserNameProof, _Mapping]] = ..., deleted_username_proof: _Optional[_Union[_username_proof_pb2.UserNameProof, _Mapping]] = ..., username_proof_message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ..., deleted_username_proof_message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...) -> None: ...

class PruneMessageBody(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    def __init__(self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...) -> None: ...

class RevokeMessageBody(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    def __init__(self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...) -> None: ...

class HubEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
USERNAME_TYPE_ENS_L1: UserNameType
USERNAME_TYPE_FNAME: UserNameType
USERNAME_TYPE_NONE: UserNameType

class UserNameProof(_message.Message):
    __slots__ = ["fid", "name", "owner", "signature", "timestamp", "type"]
    FID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    name: bytes
    owner: bytes
    signature: bytes
    timestamp: int
    type: UserNameType
    def __init__(self, timestamp: _Optional[int] = ..., name: _Optional[bytes] = ..., owner: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., fid: _Optional[int] = ..., type: _Optional[_Union[UserNameType, str]] = ...) -> None: ...

class UserNameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

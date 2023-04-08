# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: request_response.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import message_pb2 as message__pb2
import hub_event_pb2 as hub__event__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16request_response.proto\x1a\rmessage.proto\x1a\x0fhub_event.proto\"\x07\n\x05\x45mpty\"X\n\x10SubscribeRequest\x12\"\n\x0b\x65vent_types\x18\x01 \x03(\x0e\x32\r.HubEventType\x12\x14\n\x07\x66rom_id\x18\x02 \x01(\x04H\x00\x88\x01\x01\x42\n\n\x08_from_id\"\x1a\n\x0c\x45ventRequest\x12\n\n\x02id\x18\x01 \x01(\x04\"Z\n\x0fHubInfoResponse\x12\x0f\n\x07version\x18\x01 \x01(\t\x12\x11\n\tis_synced\x18\x02 \x01(\x08\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x11\n\troot_hash\x18\x04 \x01(\t\"{\n\x18TrieNodeMetadataResponse\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\x12\x14\n\x0cnum_messages\x18\x02 \x01(\x04\x12\x0c\n\x04hash\x18\x03 \x01(\t\x12+\n\x08\x63hildren\x18\x04 \x03(\x0b\x32\x19.TrieNodeMetadataResponse\"l\n\x18TrieNodeSnapshotResponse\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\x12\x17\n\x0f\x65xcluded_hashes\x18\x02 \x03(\t\x12\x14\n\x0cnum_messages\x18\x03 \x01(\x04\x12\x11\n\troot_hash\x18\x04 \x01(\t\" \n\x0eTrieNodePrefix\x12\x0e\n\x06prefix\x18\x01 \x01(\x0c\"\x1b\n\x07SyncIds\x12\x10\n\x08sync_ids\x18\x01 \x03(\x0c\"\x89\x01\n\nFidRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x16\n\tpage_size\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x03 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x04 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"}\n\x0b\x46idsRequest\x12\x16\n\tpage_size\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x02 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x03 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"N\n\x0c\x46idsResponse\x12\x0c\n\x04\x66ids\x18\x01 \x03(\x04\x12\x1c\n\x0fnext_page_token\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\x12\n\x10_next_page_token\"`\n\x10MessagesResponse\x12\x1a\n\x08messages\x18\x01 \x03(\x0b\x32\x08.Message\x12\x1c\n\x0fnext_page_token\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x42\x12\n\x10_next_page_token\"\xa0\x01\n\x14\x43\x61stsByParentRequest\x12\x18\n\x07\x63\x61st_id\x18\x01 \x01(\x0b\x32\x07.CastId\x12\x16\n\tpage_size\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\npage_token\x18\x03 \x01(\x0cH\x01\x88\x01\x01\x12\x14\n\x07reverse\x18\x04 \x01(\x08H\x02\x88\x01\x01\x42\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"^\n\x0fReactionRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12$\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionType\x12\x18\n\x07\x63\x61st_id\x18\x03 \x01(\x0b\x32\x07.CastId\"\xd1\x01\n\x15ReactionsByFidRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12)\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionTypeH\x00\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x02\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x03\x88\x01\x01\x42\x10\n\x0e_reaction_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"\xdf\x01\n\x16ReactionsByCastRequest\x12\x18\n\x07\x63\x61st_id\x18\x01 \x01(\x0b\x32\x07.CastId\x12)\n\rreaction_type\x18\x02 \x01(\x0e\x32\r.ReactionTypeH\x00\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x17\n\npage_token\x18\x04 \x01(\x0cH\x02\x88\x01\x01\x12\x14\n\x07reverse\x18\x05 \x01(\x08H\x03\x88\x01\x01\x42\x10\n\x0e_reaction_typeB\x0c\n\n_page_sizeB\r\n\x0b_page_tokenB\n\n\x08_reverse\"E\n\x0fUserDataRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12%\n\x0euser_data_type\x18\x02 \x01(\x0e\x32\r.UserDataType\"(\n\x18NameRegistryEventRequest\x12\x0c\n\x04name\x18\x01 \x01(\x0c\"3\n\x13VerificationRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0c\",\n\rSignerRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\x12\x0e\n\x06signer\x18\x02 \x01(\x0c\"%\n\x16IdRegistryEventRequest\x12\x0b\n\x03\x66id\x18\x01 \x01(\x04\"2\n\x1fIdRegistryEventByAddressRequest\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'request_response_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EMPTY._serialized_start=58
  _EMPTY._serialized_end=65
  _SUBSCRIBEREQUEST._serialized_start=67
  _SUBSCRIBEREQUEST._serialized_end=155
  _EVENTREQUEST._serialized_start=157
  _EVENTREQUEST._serialized_end=183
  _HUBINFORESPONSE._serialized_start=185
  _HUBINFORESPONSE._serialized_end=275
  _TRIENODEMETADATARESPONSE._serialized_start=277
  _TRIENODEMETADATARESPONSE._serialized_end=400
  _TRIENODESNAPSHOTRESPONSE._serialized_start=402
  _TRIENODESNAPSHOTRESPONSE._serialized_end=510
  _TRIENODEPREFIX._serialized_start=512
  _TRIENODEPREFIX._serialized_end=544
  _SYNCIDS._serialized_start=546
  _SYNCIDS._serialized_end=573
  _FIDREQUEST._serialized_start=576
  _FIDREQUEST._serialized_end=713
  _FIDSREQUEST._serialized_start=715
  _FIDSREQUEST._serialized_end=840
  _FIDSRESPONSE._serialized_start=842
  _FIDSRESPONSE._serialized_end=920
  _MESSAGESRESPONSE._serialized_start=922
  _MESSAGESRESPONSE._serialized_end=1018
  _CASTSBYPARENTREQUEST._serialized_start=1021
  _CASTSBYPARENTREQUEST._serialized_end=1181
  _REACTIONREQUEST._serialized_start=1183
  _REACTIONREQUEST._serialized_end=1277
  _REACTIONSBYFIDREQUEST._serialized_start=1280
  _REACTIONSBYFIDREQUEST._serialized_end=1489
  _REACTIONSBYCASTREQUEST._serialized_start=1492
  _REACTIONSBYCASTREQUEST._serialized_end=1715
  _USERDATAREQUEST._serialized_start=1717
  _USERDATAREQUEST._serialized_end=1786
  _NAMEREGISTRYEVENTREQUEST._serialized_start=1788
  _NAMEREGISTRYEVENTREQUEST._serialized_end=1828
  _VERIFICATIONREQUEST._serialized_start=1830
  _VERIFICATIONREQUEST._serialized_end=1881
  _SIGNERREQUEST._serialized_start=1883
  _SIGNERREQUEST._serialized_end=1927
  _IDREGISTRYEVENTREQUEST._serialized_start=1929
  _IDREGISTRYEVENTREQUEST._serialized_end=1966
  _IDREGISTRYEVENTBYADDRESSREQUEST._serialized_start=1968
  _IDREGISTRYEVENTBYADDRESSREQUEST._serialized_end=2018
# @@protoc_insertion_point(module_scope)

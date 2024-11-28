import os
import time

from dotenv import load_dotenv
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from eth_account import Account

from src.hub_py.signers import Ed25519Signer, EIP712Signer
from src.hub_py.client import get_insecure_client, get_ssl_client
from src.hub_py.generated.rpc_pb2_grpc import HubServiceStub
from src.hub_py.generated.message_pb2 import FarcasterNetwork

load_dotenv('../../.env')


def get_env_client(hub_address: str = os.getenv('FARCASTER_HUB'), use_async: bool = False, ssl: bool = False) -> HubServiceStub:
    ssl = True if os.getenv("FARCASTER_USE_SSL") == "true" else ssl
    return (
        get_ssl_client(hub_address, use_async)
        if ssl
        else get_insecure_client(hub_address, use_async)
    )


def get_env_signer() -> Ed25519Signer:
    if os.getenv("FARCASTER_SIGNER_KEY"):
        signer = Ed25519Signer(
            SigningKey(os.environ["FARCASTER_SIGNER_KEY"], encoder=HexEncoder)
        )
    else:
        signer = Ed25519Signer.generate()
        print(f"Signer private key: {signer.private_key(encoder=HexEncoder)}")
    print(f"Signer public key: {signer.public_key(encoder=HexEncoder)}")
    return signer


def get_env_mnemonic_signer() -> EIP712Signer:
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(os.environ["FARCASTER_MNEMONIC"])
    print(f"Farcaster address: {account.address}")
    return EIP712Signer(account)


def get_env_fid() -> int:
    fid = int(os.environ["FARCASTER_ID"])
    print(f"Farcaster ID: {fid}")
    return fid


def get_env_network() -> FarcasterNetwork:
    return getattr(FarcasterNetwork, os.environ["FARCASTER_NETWORK"].upper())

def covert_farcaster_timestamp() -> int:
    epoch = 1609459200
    result = int(time.time()) - epoch
    return result

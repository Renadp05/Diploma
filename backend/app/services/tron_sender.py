import time

from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

from app.core.settings import get_optional_setting, get_setting


def _network_endpoint(network: str) -> str:
    network = network.strip().lower()

    if network == "mainnet":
        return "https://api.trongrid.io"
    if network == "shasta":
        return "https://api.shasta.trongrid.io"
    if network == "nile":
        return "https://nile.trongrid.io"

    raise ValueError(f"Unsupported TRON network: {network}")


def _get_client_and_wallet():
    network = get_setting("TRON_NETWORK", "shasta").strip().lower()
    private_key_hex = get_setting("TRON_PRIVATE_KEY").strip().strip('"').strip("'")
    api_key = get_optional_setting("TRON_API_KEY")

    provider = HTTPProvider(
        endpoint_uri=_network_endpoint(network),
        api_key=api_key if api_key else None,
    )

    client = Tron(provider=provider)
    private_key = PrivateKey(bytes.fromhex(private_key_hex))
    sender_address = private_key.public_key.to_base58check_address()

    return client, private_key, sender_address, network


def get_wallet_info() -> dict:
    try:
        client, _, sender_address, network = _get_client_and_wallet()
        balance_sun = client.get_account_balance(sender_address)

        return {
            "status": "success",
            "network": network,
            "address": sender_address,
            "balance_sun": balance_sun,
            "timestamp": int(time.time()),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


def send_trx(to_address: str, amount_sun: int) -> dict:
    if not to_address:
        return {"status": "error", "message": "to_address is required"}

    if amount_sun <= 0:
        return {"status": "error", "message": "amount_sun must be greater than 0"}

    try:
        client, private_key, sender_address, network = _get_client_and_wallet()

        txn = (
            client.trx.transfer(sender_address, to_address, amount_sun)
            .build()
            .sign(private_key)
        )

        result = txn.broadcast().wait()

        return {
            "status": "success",
            "network": network,
            "from": sender_address,
            "to": to_address,
            "amount_sun": amount_sun,
            "result": result,
            "timestamp": int(time.time()),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


def _network_endpoint(network: str) -> Optional[str]:
    if network == "mainnet":
        return "https://api.trongrid.io"
    if network == "shasta":
        return "https://api.shasta.trongrid.io"
    if network == "nile":
        return "https://nile.trongrid.io"
    return None


def _get_client_and_wallet() -> tuple[Tron, PrivateKey, str, str]:
    network = os.getenv("TRON_NETWORK", "shasta").strip().lower()
    private_key_hex = os.getenv("TRON_PRIVATE_KEY", "").strip().strip('"').strip("'")
    api_key = os.getenv("TRON_API_KEY", "").strip()

    if not private_key_hex:
        raise ValueError("TRON_PRIVATE_KEY is missing in backend/.env")

    endpoint = _network_endpoint(network)
    if endpoint is None:
        raise ValueError(f"Unsupported TRON_NETWORK: {network}")

    provider = HTTPProvider(
        endpoint_uri=endpoint,
        api_key=api_key if api_key else None,
    )
    client = Tron(provider=provider)
    priv = PrivateKey(bytes.fromhex(private_key_hex))
    sender_address = priv.public_key.to_base58check_address()
    return client, priv, sender_address, network


def _get_token_contract(client: Tron):
    token_address = os.getenv("TRC20_TOKEN_ADDRESS", "").strip()
    if not token_address:
        raise ValueError(
            "TRC20_TOKEN_ADDRESS is missing in backend/.env. "
            "Deploy the contract first and paste the returned T... address into .env."
        )
    return client.get_contract(token_address), token_address


def get_token_info() -> dict:
    client, _priv, admin_address, network = _get_client_and_wallet()
    contract, token_address = _get_token_contract(client)

    try:
        name = contract.functions.name()
        symbol = contract.functions.symbol()
        decimals = contract.functions.decimals()
        total_supply_raw = contract.functions.totalSupply()
        admin_balance_raw = contract.functions.balanceOf(admin_address)
    except Exception as exc:
        return {
            "status": "error",
            "network": network,
            "contract": token_address,
            "message": f"Failed to read token state: {exc}",
        }

    scale = 10 ** int(decimals)
    return {
        "status": "success",
        "network": network,
        "contract": token_address,
        "admin_address": admin_address,
        "name": name,
        "symbol": symbol,
        "decimals": int(decimals),
        "total_supply_raw": int(total_supply_raw),
        "total_supply": int(total_supply_raw) / scale,
        "admin_balance_raw": int(admin_balance_raw),
        "admin_balance": int(admin_balance_raw) / scale,
    }


def get_balance(address: str) -> dict:
    if not address:
        return {"status": "error", "message": "address is required"}

    client, _priv, _admin, network = _get_client_and_wallet()
    contract, token_address = _get_token_contract(client)

    try:
        decimals = int(contract.functions.decimals())
        raw = int(contract.functions.balanceOf(address))
    except Exception as exc:
        return {
            "status": "error",
            "network": network,
            "contract": token_address,
            "address": address,
            "message": f"Failed to read balance: {exc}",
        }

    scale = 10 ** decimals
    return {
        "status": "success",
        "network": network,
        "contract": token_address,
        "address": address,
        "balance_raw": raw,
        "balance": raw / scale,
        "decimals": decimals,
    }


def transfer(to_address: str, amount: float) -> dict:
    if not to_address:
        return {"status": "error", "message": "to_address is required"}
    if amount <= 0:
        return {"status": "error", "message": "amount must be greater than 0"}

    client, priv, sender_address, network = _get_client_and_wallet()
    contract, token_address = _get_token_contract(client)

    try:
        decimals = int(contract.functions.decimals())
        raw_amount = int(round(amount * (10 ** decimals)))

        txn = (
            contract.functions.transfer(to_address, raw_amount)
            .with_owner(sender_address)
            .fee_limit(100_000_000)
            .build()
            .sign(priv)
        )
        result = txn.broadcast().wait()
    except Exception as exc:
        return {
            "status": "error",
            "network": network,
            "contract": token_address,
            "from": sender_address,
            "to": to_address,
            "amount": amount,
            "message": str(exc),
        }

    return {
        "status": "success",
        "network": network,
        "contract": token_address,
        "from": sender_address,
        "to": to_address,
        "amount": amount,
        "raw_amount": raw_amount,
        "tx_id": result.get("id"),
        "result": result,
    }


def mint(to_address: str, amount: float) -> dict:
    if not to_address:
        return {"status": "error", "message": "to_address is required"}
    if amount <= 0:
        return {"status": "error", "message": "amount must be greater than 0"}

    client, priv, sender_address, network = _get_client_and_wallet()
    contract, token_address = _get_token_contract(client)

    try:
        decimals = int(contract.functions.decimals())
        raw_amount = int(round(amount * (10 ** decimals)))

        txn = (
            contract.functions.mint(to_address, raw_amount)
            .with_owner(sender_address)
            .fee_limit(100_000_000)
            .build()
            .sign(priv)
        )
        result = txn.broadcast().wait()
    except Exception as exc:
        return {
            "status": "error",
            "network": network,
            "contract": token_address,
            "from": sender_address,
            "to": to_address,
            "amount": amount,
            "message": str(exc),
        }

    return {
        "status": "success",
        "network": network,
        "contract": token_address,
        "minted_to": to_address,
        "amount": amount,
        "raw_amount": raw_amount,
        "tx_id": result.get("id"),
        "result": result,
    }
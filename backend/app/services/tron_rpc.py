import requests
from app.utils.config import TRON_RPC

TRON_MAINNET_RPC = TRON_RPC
TRON_SHASTA_RPC = "https://api.shasta.trongrid.io"

def get_transaction(tx_id: str, base_url: str = TRON_RPC):
    try:
        response = requests.post(
            f"{base_url}/wallet/gettransactionbyid",
            json={"value": tx_id},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_transaction_info(tx_id: str, base_url: str = TRON_RPC):
    try:
        response = requests.get(
            f"{base_url}/walletsolidity/gettransactioninfobyid",
            params={"value": tx_id},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
    except Exception:
        return None
    return None


def get_chain_info(base_url: str = TRON_RPC):
    try:
        response = requests.get(f"{base_url}/wallet/getnowblock", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_current_block() -> int | None:
    try:
        response = requests.get(f"{TRON_RPC}/wallet/getnowblock", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["block_header"]["raw_data"]["number"]
    except Exception:
        return None
    return None


def calculate_confirmations(tx_id: str) -> int:
    current_block = get_current_block()
    tx_info = get_transaction_info(tx_id)

    if current_block is None or not tx_info:
        return 0

    tx_block = tx_info.get("blockNumber")
    if tx_block is None:
        return 0

    confirmations = current_block - tx_block + 1
    return max(confirmations, 0)


def detect_network() -> str:
    endpoints = {
        "MAINNET": TRON_MAINNET_RPC,
        "SHASTA": TRON_SHASTA_RPC,
    }

    for network_name, base_url in endpoints.items():
        try:
            response = requests.get(f"{base_url}/wallet/getnowblock", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "block_header" in data:
                    return network_name
        except requests.RequestException:
            continue

    return "UNKNOWN"
import base58


def validate_tron_address(address: str) -> dict:
    if not address or not isinstance(address, str):
        return {
            "valid": False,
            "reason": "Address is empty or invalid type"
        }

    try:
        decoded = base58.b58decode_check(address)

        if len(decoded) != 21:
            return {
                "valid": False,
                "reason": "Invalid decoded length"
            }

        if decoded[0] != 0x41:
            return {
                "valid": False,
                "reason": "Invalid TRON network prefix"
            }

        return {
            "valid": True,
            "reason": "Valid TRON address"
        }

    except Exception:
        return {
            "valid": False,
            "reason": "Invalid Base58 checksum"
        }
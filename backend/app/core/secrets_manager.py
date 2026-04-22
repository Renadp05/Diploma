import json
import os
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class SecretManagerError(Exception):
    pass


@lru_cache(maxsize=1)
def _get_secrets_client():
    region = os.getenv("AWS_REGION", "eu-central-1")
    return boto3.client("secretsmanager", region_name=region)


@lru_cache(maxsize=32)
def get_secret(secret_name: str) -> Dict[str, Any]:
    """
    Reads a JSON secret from AWS Secrets Manager and returns it as a dict.

    Example secret value:
    {
      "TRON_PRIVATE_KEY": "...",
      "DATABASE_URL": "...",
      "SECRET_KEY": "..."
    }
    """
    if not secret_name:
        raise SecretManagerError("Secret name is required")

    client = _get_secrets_client()

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except (ClientError, BotoCoreError) as exc:
        raise SecretManagerError(f"Failed to read secret '{secret_name}': {exc}") from exc

    secret_string: Optional[str] = response.get("SecretString")
    if not secret_string:
        raise SecretManagerError(f"Secret '{secret_name}' does not contain SecretString")

    try:
        parsed = json.loads(secret_string)
    except json.JSONDecodeError as exc:
        raise SecretManagerError(
            f"Secret '{secret_name}' must be valid JSON"
        ) from exc

    if not isinstance(parsed, dict):
        raise SecretManagerError(f"Secret '{secret_name}' must decode to a JSON object")

    return parsed


def get_secret_value(secret_name: str, key: str, default: Optional[str] = None) -> str:
    """
    Returns one field from a JSON secret.
    """
    secret = get_secret(secret_name)
    value = secret.get(key, default)

    if value is None:
        raise SecretManagerError(
            f"Key '{key}' was not found in secret '{secret_name}'"
        )

    return str(value)
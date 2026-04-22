import os
from functools import lru_cache
from typing import Optional

from app.core.secrets_manager import SecretManagerError, get_secret_value


def _read_from_env(key: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value


@lru_cache(maxsize=1)
def _get_app_secret_name() -> Optional[str]:
    """
    Name of the AWS Secrets Manager secret that stores app config.
    Example:
        APP_SECRET_NAME=trc/backend/prod
    """
    return _read_from_env("APP_SECRET_NAME")


def get_setting(key: str, default: Optional[str] = None) -> str:
    """
    Reads a setting using this order:
    1. AWS Secrets Manager (if APP_SECRET_NAME is configured)
    2. Environment variable / .env fallback

    This lets local development continue to work while production uses Secrets Manager.
    """
    secret_name = _get_app_secret_name()

    if secret_name:
        try:
            return get_secret_value(secret_name, key, default)
        except SecretManagerError:
            env_value = _read_from_env(key, default)
            if env_value is None:
                raise
            return env_value

    env_value = _read_from_env(key, default)
    if env_value is None:
        raise ValueError(f"Missing required setting: {key}")

    return env_value


def get_optional_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Same as get_setting, but returns None if the value is missing.
    """
    secret_name = _get_app_secret_name()

    if secret_name:
        try:
            return get_secret_value(secret_name, key, default)
        except SecretManagerError:
            return _read_from_env(key, default)

    return _read_from_env(key, default)
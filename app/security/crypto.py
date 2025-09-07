import base64
import hashlib
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings


_settings = get_settings()


def _get_fernet() -> Fernet:
    key_material = _settings.encryption_key
    if not key_material:
        # Derive a deterministic but insecure key from SECRET_KEY as fallback
        key_material = _settings.secret_key
    # Derive 32-byte key using SHA256, then urlsafe base64 encode
    digest = hashlib.sha256(key_material.encode("utf-8")).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_value(plaintext: str) -> str:
    f = _get_fernet()
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_value(ciphertext: str) -> Optional[str]:
    f = _get_fernet()
    try:
        value = f.decrypt(ciphertext.encode("utf-8"))
        return value.decode("utf-8")
    except (InvalidToken, ValueError):
        return None
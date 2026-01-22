import hashlib
import uuid
from typing import Optional


def normalize_identifier(identifier: str) -> str:
    return identifier.strip().lower()


def hash_identifier(identifier: str) -> str:
    normalized = normalize_identifier(identifier)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_or_create_user_id(identifier: Optional[str] = None) -> str:
    """
    If identifier provided (email / phone / username) → hashed ID
    Else → auto-generate UUID for new user
    """
    if identifier:
        return hash_identifier(identifier)
    return str(uuid.uuid4())

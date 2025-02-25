import hashlib


def hash_password(password: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    return sha256_hash.hexdigest()


def verify_password(password: str, hashed_password: str) -> bool: ...

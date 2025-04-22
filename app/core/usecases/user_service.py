import hashlib
from app.infra.entities.user_entity import user_entity
from app.infra.provider import user_provider

def hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(stored_hash: str, attempted_password: str) -> bool:
    return stored_hash == attempted_password

def autenticar_login(username: str, password : str):
    passwordCoded = hash_password(password)
    user = user_provider.get_by_username_password(username)
    if not user:
        return None
    if verify_password(user.password, passwordCoded):
        return user
    return None   

def create(data: dict):
    return user_provider.create(data)

def get_all():
    return user_provider.get_all()
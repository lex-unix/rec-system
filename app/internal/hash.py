from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def compare_hash(plaintext: str, hash: str) -> bool:
    return pwd_context.verify(plaintext, hash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

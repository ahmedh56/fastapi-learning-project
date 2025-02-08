from passlib.context import CryptContext

pws_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return pws_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    return pws_context.verify(plain_password, hashed_password)

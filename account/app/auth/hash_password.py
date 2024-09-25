from passlib.context import CryptContext


class HashPassword:
    context = CryptContext(schemes=['bcrypt'])

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.context.hash(password)
    

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.context.verify(plain_password, hashed_password)
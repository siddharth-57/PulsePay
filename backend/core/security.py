# What This Step Does: Password Hashing Infrastructure
# Stores passwords securely using hashing and verification

from passlib.context import (
    CryptContext
)

from jose import jwt

from datetime import datetime
from datetime import timedelta

from backend.core.config import (
    settings
)

from jose import JWTError

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
):

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    user_id: str
):

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=settings.JWT_EXPIRATION_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )

        return payload

    except JWTError:

        return None
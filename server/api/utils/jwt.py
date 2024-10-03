import datetime as dt
from jose import jwt
from typing import Any
from api.config import settings


def encode_token(payload: dict) -> str:
    return jwt.encode(payload, settings.TOKEN_SECRET, settings.ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.ALGORITHM])


def create_token(sub: Any) -> str:
    initiated_at: dt.datetime = dt.datetime.now()
    expires_on: dt.datetime = dt.datetime.now() + dt.timedelta(
        seconds=settings.EXPIRATION_SECONDS
    )

    token_payload = {'exp': expires_on, 'iat': initiated_at, 'sub': str(sub)}

    access_token: str = encode_token(token_payload)
    return access_token

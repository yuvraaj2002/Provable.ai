import traceback
from datetime import UTC, datetime, timedelta
from app.core.config import settings
from jose import JWTError,jwt

async def create_access_token(data:dict):
    try:
        to_encode = data.copy()
        expiry_time = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expiry_time})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KET, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        traceback.print_exc()
        return None


async def verify_token(token:str):
    try:
        payload = jwt.decode(token, settings.SECRET_KET, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        traceback.print_exc()
        return None

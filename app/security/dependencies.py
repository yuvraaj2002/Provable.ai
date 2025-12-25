import traceback
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException,status
from .jwt_management import verify_token
from app.helpers import UserHelper
from app.core.database import get_db

# Security scheme for Bearer token
security = HTTPBearer()

async def get_current_auth_user(credentials: HTTPAuthorizationCredentials = Depends(security),db_session=Depends(get_db),user_helper=Depends(UserHelper)):
    try:
        token = credentials.credentials
        payload = await verify_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("id",None)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Getting the user data from the database
        user_data = await user_helper.get_user(user_id,db_session)
        if user_data is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return user_data

    except Exception as e:
        traceback.print_exc()
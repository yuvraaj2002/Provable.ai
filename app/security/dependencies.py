import traceback
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException,status
from .jwt_management import verify_token
from app.helpers import UserHelper, ApiKeyHelper
from app.core.database import get_db

# Security scheme for Bearer token
security = HTTPBearer()
user_helper=UserHelper()
api_key_helper=ApiKeyHelper()




async def _get_current_user(credentials: HTTPAuthorizationCredentials, db_session, check_admin: bool = False):
    """
    Internal function to get current user with optional admin check.
    """
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
    
    # Checking if the user is admin user when check_admin is True
    if check_admin and not user_data.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return user_data

async def get_current_auth_user(credentials: HTTPAuthorizationCredentials = Depends(security), db_session=Depends(get_db)):
    try:
        return await _get_current_user(credentials, db_session, check_admin=False)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e

async def get_current_admin_user(credentials: HTTPAuthorizationCredentials = Depends(security), db_session=Depends(get_db)):
    try:
        return await _get_current_user(credentials, db_session, check_admin=True)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e

async def get_current_user_from_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db_session=Depends(get_db)
):
    """
    Dependency function to authenticate user via API key from Authorization header.
    Extracts and verifies the API key, then returns the authenticated user data.
    Raises HTTPException if API key is invalid or user is not found.
    """
    try:
        # Check if credentials were provided
        if credentials is None:
            print("No credentials provided in get_current_user_from_api_key")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key is required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extract the API key from the Bearer token
        api_key = credentials.credentials
        print(f"Received API key (first 20 chars): {api_key[:20] if api_key else 'None'}...")
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key is required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify the API key against the database and get the associated user_id
        user_id = await api_key_helper.verify_api_key(api_key, db_session)
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Retrieve the user data from the database
        user_data = await user_helper.get_user(user_id, db_session)
        
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        ) from e
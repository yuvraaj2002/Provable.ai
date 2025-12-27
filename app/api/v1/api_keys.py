import traceback
from fastapi import Depends, HTTPException,APIRouter,Request
from fastapi.responses import JSONResponse
from app.schema.api_keys_schema import CreateAPIKeyRequest
from app.security.dependencies import get_current_auth_user
from app.helpers import ApiKeyHelper
from app.core.database import get_db

router = APIRouter(prefix="/api/v1/api_keys", tags=["api_keys"])
api_key_helper = ApiKeyHelper()

@router.post("/")
async def create_api_key(request:CreateAPIKeyRequest,current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        api_key = await api_key_helper.create_key(request.key_name,current_auth_user.id,db_session)
        if api_key is not None:
            return JSONResponse(content={"api_key": api_key, "message": "API key created successfully"},status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to create API key")
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/")
async def get_api_keys(current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        api_keys = await api_key_helper.get_keys(current_auth_user.id,db_session)
        if api_keys is not None:
            return JSONResponse(content={"api_keys": api_keys},status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch API keys")
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.delete("/{key_id}")
async def delete_api_key(key_id:str,current_auth_user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        deleted = await api_key_helper.delete_key(key_id,current_auth_user.id,db_session)
        if deleted:
            return JSONResponse(content={"message": "API key deleted successfully"},status_code=200)
        else:
            raise HTTPException(status_code=404, detail="API key not found or you don't have permission to delete it")
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
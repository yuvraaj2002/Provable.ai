import traceback
from app.core.auth import oauth
from fastapi import FastAPI, APIRouter,HTTPException,Request,Depends
from fastapi.responses import JSONResponse
from app.helpers import UserHelper
from app.core.database import get_db
from app.security.dependencies import get_current_auth_user



router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/google-login")
async def google_login(request: Request):
    try:
        redirect_uri = request.url_for('google_callback')
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    
@router.get("/google-callback")
async def google_callback(request: Request,user_helper=Depends(UserHelper),db_session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        access_token = await user_helper.get_or_create(user_data=user,db_session=db_session)
        return JSONResponse(content={"access_token": access_token}, status_code=200)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


# Creating the endpoint to show the current user info
@router.get("/me")
async def user_data(user=Depends(get_current_auth_user),db_session=Depends(get_db)):
    try:
        return user
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
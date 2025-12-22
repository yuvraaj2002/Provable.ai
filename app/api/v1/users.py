import traceback
from app.core.auth import oauth
from fastapi import FastAPI, APIRouter,HTTPException,Request
from fastapi.responses import JSONResponse

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
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = await oauth.google.parse_id_token(request, token)
        print("User info:", user)
        return JSONResponse(content={"user": user})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
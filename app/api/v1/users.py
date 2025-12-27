import traceback
from app.core.auth import oauth
from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.helpers import UserHelper
from app.core.database import get_db
from app.schema.user_schema import LoginRequest, SignupRequest
from app.security.dependencies import get_current_auth_user
from app.security.jwt_management import verify_token
from app.security.password_management import PasswordManagement
from fastapi.concurrency import run_in_threadpool

# Instantiate classes at the top
router = APIRouter(prefix="/api/v1/users", tags=["users"])
user_helper = UserHelper()
password_management = PasswordManagement()

@router.get("/google-login")
async def google_login(request: Request):
    try:
        redirect_uri = request.url_for('google_callback')
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    
@router.get("/google-callback")
async def google_callback(request: Request,db_session=Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        access_token = await user_helper.get_or_create(user_data=user,db_session=db_session)
        return JSONResponse(content={"access_token": access_token}, status_code=200)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@router.post("/login")
async def user_login(request:LoginRequest,db_session=Depends(get_db)):
    try:
        # Extracting the email and password from request
        email = request.email
        password = request.password

        # Verifying the password + generating the access token
        access_token = await user_helper.verify_password_generate_token(email,password,db_session)
        return JSONResponse(content={"access_token": access_token},status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@router.post("/signup")
async def user_signup(request:SignupRequest,db_session=Depends(get_db)):
    try:
        # Getting username, email and password from request
        username = request.username
        email = request.email
        hashed_password = await run_in_threadpool(password_management.hash_password,request.password)

        # Creating record in pending user table and initiating the verification mail
        result = await user_helper.create_pending_user(username,email,hashed_password,db_session)
        if result:
            return JSONResponse(content={"message": "Verification mail has been sent to your registered mail."},status_code=200)
        else:
            # Email already exists or other error
            raise HTTPException(status_code=400, detail="Email already registered or invalid request")

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@router.get("/verify-mail")
async def verify_mail(token: str, db_session=Depends(get_db)):
    try:
        # Verify the token
        payload = await verify_token(token)
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid or expired verification token")
        
        # Get the pending user id from token payload
        pending_user_id = payload.get('id')
        if not pending_user_id:
            raise HTTPException(status_code=400, detail="Invalid token payload: missing user id")
        
        # Move pending user to active user
        user_created = await user_helper.move_pending_user(pending_user_id, db_session)
        if user_created:
            return JSONResponse(
                content={"message": "Email verified successfully. Please login to continue."}, 
                status_code=200
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail="Verification failed. The link may have already been used or is invalid."
            )

    except HTTPException:
        raise
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
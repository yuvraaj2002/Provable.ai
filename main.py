from fastapi import FastAPI
from app import users_router
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.include_router(users_router)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Safety Application!"}

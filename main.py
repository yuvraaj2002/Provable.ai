from fastapi import FastAPI
from app import users_router,api_keys_router,agent_router
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware first (executes last, wrapping all responses)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add Session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

# Include routers
app.include_router(users_router)
app.include_router(api_keys_router)
app.include_router(agent_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Safety Application!"}

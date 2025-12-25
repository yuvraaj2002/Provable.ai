from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings # Assuming database_url is here

# 1. Create the engine (Supabase uses PostgreSQL)
engine = create_async_engine(settings.DATABASE_URL,pool_pre_ping=True,pool_size=10,max_overflow=20)

# 2. Create a session factory
SessionLocal = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

# 3. Base class for your models to inherit from
Base = declarative_base()

# 4. Dependency to get a DB session in your routes
async def get_db():
    async with SessionLocal() as session:
        yield session
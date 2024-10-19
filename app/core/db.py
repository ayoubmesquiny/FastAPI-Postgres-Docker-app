from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base

engine = create_async_engine(settings.DB_URL, future=True)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
    )

async def create_db_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

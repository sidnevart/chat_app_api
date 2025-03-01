
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
import logging

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/chatdb"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            logging.info("Yielding database session")
            return session
    except Exception as e:
        logging.error(f"Error creating database session: {e}")
        raise e

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




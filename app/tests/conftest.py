import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..database import Base

@pytest.fixture(scope="function")
def event_loop():
    """Создаем новый event loop для каждого теста."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """Создаем новую сессию для каждого теста с новой базой данных в памяти."""
    # Используем новую in-memory SQLite базу для каждого теста
    DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/chatdb"
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Создаем сессию
    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        
    # Очищаем после теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()
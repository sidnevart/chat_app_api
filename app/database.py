
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
import logging

# Базовый класс для моделей
Base = declarative_base()

# Настройка асинхронного движка SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/chatdb"

# Создание асинхронного движка
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создание асинхронной сессии
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии
async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            logging.info("Yielding database session")
            return session
    except Exception as e:
        logging.error(f"Error creating database session: {e}")
        raise e

# Функция для создания всех таблиц в базе данных
async def create_tables():
    # Подключаемся к базе данных и выполняем создание таблиц
    async with engine.begin() as conn:
        # Синхронное выполнение создания таблиц
        await conn.run_sync(Base.metadata.create_all)

"""# Запуск создания таблиц
# Для этого нужно использовать asyncio.run(create_tables()) в вашем приложении, чтобы создать таблицы при старте.
if __name__ == "__main__":
    asyncio.run(create_tables())"""


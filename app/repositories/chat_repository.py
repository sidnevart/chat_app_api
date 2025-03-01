from sqlalchemy.ext.asyncio import AsyncSession
from ..models.chat import Chat
from sqlalchemy.future import select
from ..schemas.chat import ChatCreate
import logging

class ChatRepository:
    def __init__(self, db: AsyncSession):
        if db is None:
            logging.error("Received None for db in ChatRepository")
        self.db = db

    async def create_chat(self, chat: ChatCreate):
        logging.info(f"Received database session: {chat} {chat.name} {chat.type}")
        if self.db is None:
            logging.error("Database session is None in create_chat")
            raise ValueError("Database session is None")
        db_chat = Chat(name=chat.name, type=chat.type)
        self.db.add(db_chat)
        await self.db.commit()
        await self.db.refresh(db_chat)
        return db_chat

    async def get_chat_by_id(self, chat_id: int):
        if self.db is None:
            logging.error("Database session is None in get_chat_by_id")
            raise ValueError("Database session is None")
        result = await self.db.execute(select(Chat).filter(Chat.id == chat_id))
        return result.scalars().first()
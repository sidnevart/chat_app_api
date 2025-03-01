from sqlalchemy.ext.asyncio import AsyncSession
from ..models.message import Message
from ..schemas.message import MessageCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select

class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(self, message: MessageCreate):
        db_message = Message(**message.dict())
        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def mark_message_as_read(self, message_id: int):
        result = await self.db.execute(select(Message).filter(Message.id == message_id))
        message = result.scalars().first()
        if message:
            message.is_read = True
            await self.db.commit()
            await self.db.refresh(message)
        return message
    
    async def create_message(self, message: MessageCreate):
        db_message = Message(**message.dict())
        try:
            self.db.add(db_message)
            await self.db.commit()
            await self.db.refresh(db_message)
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Duplicate message detected")
        return db_message

    async def get_messages_by_chat_id(self, chat_id: int, limit: int = 100, offset: int = 0):
        stmt = select(Message).filter(Message.chat_id == chat_id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
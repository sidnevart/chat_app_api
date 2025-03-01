from ..repositories.message_repository import MessageRepository
from ..schemas.message import MessageCreate, MessageResponse
from ..database import get_db

class MessageService:
    def __init__(self, db):
        self.repo = MessageRepository(db)

    async def create_message(self, message: MessageCreate):
        return await self.repo.create_message(message)

    async def get_messages_by_chat_id(self, chat_id: int, limit: int = 100, offset: int = 0):
        return await self.repo.get_messages_by_chat_id(chat_id, limit, offset)
from ..models.chat import Chat
from ..repositories.chat_repository import ChatRepository
from ..schemas.chat import ChatCreate, ChatResponse
from ..database import get_db

class ChatService:
    def __init__(self, db):
        self.repo = ChatRepository(db)

    async def create_chat(self, chat: Chat):
        return await self.repo.create_chat(chat)

    async def get_chat_by_id(self, chat_id: int):
        return await self.repo.get_chat_by_id(chat_id)
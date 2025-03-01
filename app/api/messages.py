from fastapi import APIRouter, Depends, HTTPException
from ..schemas.message import MessageCreate, MessageResponse
from ..services.message_service import MessageService
from ..database import get_db
from ..repositories.message_repository import MessageRepository

router = APIRouter()

@router.post("/messages/", response_model=MessageResponse)
async def create_message(message: MessageCreate, db = Depends(get_db)):
    service = MessageService(db)
    return await service.create_message(message)

@router.get("/history/{chat_id}", response_model=list[MessageResponse])
async def get_chat_history(chat_id: int, limit: int = 100, offset: int = 0, db = Depends(get_db)):
    service = MessageService(db)
    return await service.get_messages_by_chat_id(chat_id, limit, offset)

@router.post("/messages/{message_id}/mark_as_read", response_model=MessageResponse)
async def mark_message_as_read(message_id: int, db = Depends(get_db)):
    repo = MessageRepository(db)
    message = await repo.mark_message_as_read(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
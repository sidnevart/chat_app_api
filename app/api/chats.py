from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.chat import ChatCreate, ChatResponse
from ..repositories.chat_repository import ChatRepository
from ..database import get_db
import logging

router = APIRouter()

@router.post("/chats/", response_model=ChatResponse)
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db)):
    logging.info(f"Received database session: {db}")
    if db is None:
        logging.error("Database session is None")
        raise HTTPException(status_code=500, detail="Database session is None")
    repo = ChatRepository(db)
    db_chat = await repo.create_chat(chat)
    return db_chat

@router.get("/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    logging.info(f"Received database session: {db}")
    if db is None:
        logging.error("Database session is None")
        raise HTTPException(status_code=500, detail="Database session is None")
    repo = ChatRepository(db)
    db_user = await repo.get_chat_by_id(chat_id)
    return db_user
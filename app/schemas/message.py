from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    text: str

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True
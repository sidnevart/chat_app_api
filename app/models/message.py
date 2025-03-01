from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID
import uuid
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID, unique=True, default=uuid.uuid4)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    chat = relationship("Chat", back_populates="messages")
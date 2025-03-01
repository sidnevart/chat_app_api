from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # "private" || "group"
    messages = relationship("Message", back_populates="chat")
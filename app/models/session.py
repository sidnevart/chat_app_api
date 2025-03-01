from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class UserSession(Base):
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(String, unique=True, index=True)
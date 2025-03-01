from pydantic import BaseModel, EmailStr
from typing import Optional 


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True  # Это важно для использования from_orm


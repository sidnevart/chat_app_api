from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate, hashed_password: str):
        db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        try:
            await self.db.commit() 
            await self.db.refresh(db_user) 
            return db_user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")

    async def get_user_by_username(self, username: str):
        stmt = select(User).filter(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalars().first()
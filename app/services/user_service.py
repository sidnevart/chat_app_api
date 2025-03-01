from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserInDB
from ..database import get_db

class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    async def create_user(self, user: UserCreate):
        return await self.repo.create_user(user)

    async def get_user_by_username(self, username: str):
        return await self.repo.get_user_by_username(username)
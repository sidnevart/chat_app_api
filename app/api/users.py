from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.user_repository import UserRepository
from ..auth.security import get_current_user, get_password_hash  # Import the get_current_user function
from ..schemas.user import UserCreate, UserInDB
from ..services.user_service import UserService
from ..database import get_db

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user_repo = UserRepository(db)
    db_user = await user_repo.create_user(user, hashed_password)
    return db_user



@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
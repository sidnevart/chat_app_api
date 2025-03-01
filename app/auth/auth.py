from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth.security import create_access_token, get_password_hash, verify_password
from ..schemas.user import UserCreate, UserInDB
from ..repositories.user_repository import UserRepository
from ..database import get_db

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = await UserRepository(db).get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user_repo = UserRepository(db)
    db_user = await user_repo.create_user(user, hashed_password)
    return db_user

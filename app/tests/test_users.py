from sqlalchemy import select
from ..models.user import User
from passlib.context import CryptContext
import pytest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.mark.asyncio
async def test_register_user(db_session):
    hashed_password = pwd_context.hash("testpass")
    user = User(username="testuser", email="test@example.com", hashed_password=hashed_password)
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    result = await db_session.execute(select(User).where(User.id == user.id))
    fetched_user = result.scalars().first()
    
    assert fetched_user is not None
    assert fetched_user.username == "testuser"
    assert fetched_user.email == "test@example.com"
    assert pwd_context.verify("testpass", fetched_user.hashed_password)

@pytest.mark.asyncio
async def test_get_user_by_username(db_session):
    hashed_password = pwd_context.hash("findpass")
    user = User(username="finduser", email="find@example.com", hashed_password=hashed_password)
    
    db_session.add(user)
    await db_session.commit()
    
    result = await db_session.execute(select(User).where(User.username == "finduser"))
    found_user = result.scalars().first()
    
    assert found_user is not None
    assert found_user.username == "finduser"
    assert found_user.email == "find@example.com"
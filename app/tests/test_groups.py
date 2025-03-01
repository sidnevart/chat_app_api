from sqlalchemy import select
from ..models.group import Group
from ..models.user import User
import pytest

@pytest.mark.asyncio
async def test_create_group(db_session):
    user = User(username="testuser", email="test@example.com", hashed_password="hashedpass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    group = Group(name="Test Group", creator_id=user.id)
    db_session.add(group)
    await db_session.commit()
    await db_session.refresh(group)
    
    result = await db_session.execute(select(Group).where(Group.id == group.id))
    fetched_group = result.scalars().first()
    
    assert fetched_group is not None
    assert fetched_group.name == "Test Group"
    assert fetched_group.creator_id == user.id

@pytest.mark.asyncio
async def test_get_group(db_session):
    user = User(username="testuser2", email="test2@example.com", hashed_password="hashedpass")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    group = Group(name="Test Group Get", creator_id=user.id)
    db_session.add(group)
    await db_session.commit()
    await db_session.refresh(group)
    
    result = await db_session.execute(select(Group).where(Group.id == group.id))
    fetched_group = result.scalars().first()
    
    assert fetched_group is not None
    assert fetched_group.name == "Test Group Get"
    assert fetched_group.creator_id == user.id
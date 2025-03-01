from sqlalchemy import select
from ..models.chat import Chat
import pytest

@pytest.mark.asyncio
async def test_create_chat(db_session):
    chat = Chat(name="Test Chat", type="group")
    
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)
    
    # Проверяем, что чат создан
    result = await db_session.execute(select(Chat).where(Chat.id == chat.id))
    fetched_chat = result.scalars().first()
    
    assert fetched_chat is not None
    assert fetched_chat.name == "Test Chat"
    assert fetched_chat.type == "group"

@pytest.mark.asyncio
async def test_get_chat(db_session):
    chat = Chat(name="Find Chat", type="private")
    
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(chat)
    
    # Получаем чат по ID
    result = await db_session.execute(select(Chat).where(Chat.id == chat.id))
    fetched_chat = result.scalars().first()
    
    assert fetched_chat is not None
    assert fetched_chat.name == "Find Chat"
    assert fetched_chat.type == "private"

@pytest.mark.asyncio
async def test_get_chats_by_type(db_session):
    # Создаем несколько чатов разных типов
    group_chat = Chat(name="Group Chat", type="group")
    private_chat1 = Chat(name="Private Chat 1", type="private")
    private_chat2 = Chat(name="Private Chat 2", type="private")
    
    db_session.add_all([group_chat, private_chat1, private_chat2])
    await db_session.commit()
    
    # Получаем все приватные чаты
    result = await db_session.execute(select(Chat).where(Chat.type == "private"))
    private_chats = result.scalars().all()
    
    assert len(private_chats) >= 2  # может быть больше из-за предыдущих тестов
    for chat in private_chats:
        assert chat.type == "private"
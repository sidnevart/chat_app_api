from sqlalchemy import select
from ..models.message import Message
from ..models.chat import Chat
from ..models.user import User
import pytest

@pytest.mark.asyncio
async def test_create_message(db_session):
    user = User(username="messageuser", email="message@example.com", hashed_password="hashedpass")
    chat = Chat(name="Message Chat", type="group")
    db_session.add(user)
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(user)
    await db_session.refresh(chat)
    
    message = Message(chat_id=chat.id, sender_id=user.id, text="Hello, World!")
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    
    result = await db_session.execute(select(Message).where(Message.id == message.id))
    fetched_message = result.scalars().first()
    
    assert fetched_message is not None
    assert fetched_message.text == "Hello, World!"
    assert fetched_message.chat_id == chat.id
    assert fetched_message.sender_id == user.id

@pytest.mark.asyncio
async def test_get_message_history(db_session):
    user = User(username="historyuser", email="history@example.com", hashed_password="hashedpass")
    chat = Chat(name="History Chat", type="group")
    db_session.add(user)
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(user)
    await db_session.refresh(chat)
    
    messages = [
        Message(chat_id=chat.id, sender_id=user.id, text=f"Message {i}")
        for i in range(3)
    ]
    for msg in messages:
        db_session.add(msg)
    await db_session.commit()
    
    result = await db_session.execute(select(Message).where(Message.chat_id == chat.id))
    fetched_messages = result.scalars().all()
    
    assert len(fetched_messages) == 3
    for i, msg in enumerate(fetched_messages):
        assert f"Message " in msg.text

@pytest.mark.asyncio
async def test_mark_message_as_read(db_session):
    user = User(username="readuser", email="read@example.com", hashed_password="hashedpass")
    chat = Chat(name="Read Chat", type="group")
    db_session.add(user)
    db_session.add(chat)
    await db_session.commit()
    await db_session.refresh(user)
    await db_session.refresh(chat)
    
    message = Message(chat_id=chat.id, sender_id=user.id, text="Read me!")
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    
    result = await db_session.execute(select(Message).where(Message.id == message.id))
    fetched_message = result.scalars().first()
    fetched_message.is_read = True
    await db_session.commit()

    result = await db_session.execute(select(Message).where(Message.id == message.id))
    updated_message = result.scalars().first()
    assert updated_message.is_read is True
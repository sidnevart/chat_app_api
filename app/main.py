from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends

from .models.user import User
from .api import users, chats, groups, messages
from .auth import auth
from .websockets_chat_app.chat_manager import ConnectionManager
from .utils.logger import log_requests
from .utils.error_handlers import add_error_handlers
from .database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
import os

app = FastAPI()
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Middleware для логирования
app.middleware("http")(log_requests)

# Обработчики ошибок
add_error_handlers(app)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chats.router)
app.include_router(groups.router)
app.include_router(messages.router)

# Инициализация менеджера WebSocket
manager = ConnectionManager()

@app.on_event("startup")
async def startup():
    # Создание таблиц в базе данных
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    # Закрытие соединений с базой данных или любых других ресурсов
    pass

# WebSocket обработчик
@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str, db: AsyncSession = Depends(get_db)):
    logging.info(f"WebSocket connection attempt to chat {chat_id} with token {token[:10]}...")
    
    # Проверка аутентификации и получения данных о пользователе через токен
    user = await get_user_from_token(db, token)
    if user is None:
        logging.error(f"Authentication failed for token {token[:10]}")
        await websocket.close(code=1008)
        return
    
    logging.info(f"User {user.username} authenticated successfully")
    await manager.connect(websocket, chat_id, user)
    
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received message from {user.username} in chat {chat_id}: {data}")
            await manager.broadcast(f"{user.username}: {data}", chat_id)
    except WebSocketDisconnect:
        logging.info(f"WebSocket disconnected for user {user.username}")
        manager.disconnect(websocket, chat_id)

        
# Пример функции для извлечения пользователя из токена (потребуется настроить в зависимости от вашей логики)
async def get_user_from_token(db: AsyncSession, token: str):
    try:
        # Для JWT токенов используйте декодирование
        from jose import jwt
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username = payload.get("sub")
        result = await db.execute(select(User).filter(User.username == username))
    except Exception as e:
        logging.error(f"Error decoding token: {e}")
        return None
    
    return result.scalars().first()

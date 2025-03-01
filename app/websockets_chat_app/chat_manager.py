from fastapi import WebSocket, status, HTTPException
from jose import JWTError, jwt
from dotenv import load_dotenv
from typing import Dict, List, Any
import os
import logging

# Загрузка переменных окружения
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[Dict[str, Any]]] = {}
        
    async def connect(self, websocket: WebSocket, chat_id: int, user):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
            
        # Сохраняем соединение вместе с данными пользователя
        connection_info = {"websocket": websocket, "user": user}
        self.active_connections[chat_id].append(connection_info)
        logging.info(f"User {user.username} connected to chat {chat_id}")
        
    def disconnect(self, websocket: WebSocket, chat_id: int = None):
        # Если chat_id известен
        if chat_id and chat_id in self.active_connections:
            # Найдем и удалим соединение
            for i, connection in enumerate(self.active_connections[chat_id]):
                if connection["websocket"] == websocket:
                    user = connection["user"]
                    self.active_connections[chat_id].pop(i)
                    logging.info(f"User {user.username} disconnected from chat {chat_id}")
                    break
                    
            # Если в чате больше нет соединений, удалим запись о чате
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]
        else:
            # Если chat_id неизвестен, ищем во всех чатах
            for chat_id, connections in list(self.active_connections.items()):
                for i, connection in enumerate(connections):
                    if connection["websocket"] == websocket:
                        user = connection["user"]
                        connections.pop(i)
                        logging.info(f"User {user.username} disconnected from chat {chat_id}")
                        break
                        
                # Если в чате больше нет соединений, удалим запись о чате
                if not self.active_connections[chat_id]:
                    del self.active_connections[chat_id]
                    
    async def broadcast(self, message: str, chat_id: int):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                websocket = connection["websocket"]
                await websocket.send_text(message)

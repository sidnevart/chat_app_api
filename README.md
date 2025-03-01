# Chat App - Документация

## Содержание

- Запуск проекта с помощью Docker
- Примеры запросов к API
- Тестирование в Postman
- Тестирование WebSocket

## Запуск проекта с помощью Docker

1. Клонируйте репозиторий:

```bash
git clone https://github.com/sidnevart/chat_app_api.git
cd chat_app
```

2. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d
```

3. Приложение будет доступно по адресу http://localhost:8000
4. Swagger - http://localhost:8000/docs
5. Для остановки приложения выполните:

```bash
docker-compose down
```

## Примеры запросов к API

### Регистрация пользователя

```
POST /register
```

Тело запроса:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass"
}
```

### Получение токена авторизации

```
POST /token
```

Форма данных:
- username: testuser
- password: testpass

### Создание чата

```
POST /chats/
```

Заголовки:
- Authorization: Bearer {access_token}

Тело запроса:
```json
{
  "name": "Тестовый чат",
  "type": "group"
}
```

### Создание сообщения

```
POST /messages/
```

Заголовки:
- Authorization: Bearer {access_token}

Тело запроса:
```json
{
  "chat_id": 1,
  "sender_id": 1,
  "text": "Привет, мир!"
}
```

### Получение истории сообщений

```
GET /history/{chat_id}?limit=100&offset=0
```

Заголовки:
- Authorization: Bearer {access_token}

## Тестирование в Postman

1. Импортируйте коллекцию Postman из файла postman_config.json

2. Создайте новое окружение и установите переменные:
   - `base_url`: http://localhost:8000
   - `access_token`: (заполнится автоматически после авторизации)

3. Выполните запрос "Register User" для создания нового пользователя

4. Выполните запрос "Login User" для получения токена доступа (сохранится автоматически в переменной окружения)

5. Протестируйте остальные запросы, используя полученный токен

## Тестирование WebSocket

### Через командную строку

Установите утилиту `websocat` и выполните:

```bash
websocat "ws://localhost:8000/ws/1?token=ВАШ_JWT_ТОКЕН"
```

После подключения вводите сообщения и нажимайте Enter для отправки.

### Установка утилиты websocat

#### Linux

**Способ 1**: Через менеджер пакетов Cargo (требуется установленный Rust):
```bash
cargo install websocat
```

**Способ 2**: Загрузка готового бинарного файла:
```bash
wget https://github.com/vi/websocat/releases/download/v1.11.0/websocat.x86_64-unknown-linux-musl -O websocat
chmod +x websocat
sudo mv websocat /usr/local/bin/
```

#### macOS

**Способ 1**: Через Homebrew:
```bash
brew install websocat
```

**Способ 2**: Через менеджер пакетов Cargo (требуется установленный Rust):
```bash
cargo install websocat
```

#### Windows

**Способ 1**: Скачайте готовый исполняемый файл с GitHub:
1. Перейдите на страницу https://github.com/vi/websocat/releases
2. Загрузите файл `websocat.x86_64-pc-windows-msvc.exe`
3. Переименуйте файл в `websocat.exe`
4. Переместите файл в директорию, которая включена в переменную PATH, или добавьте директорию с файлом в PATH

**Способ 2**: Через менеджер пакетов Cargo (требуется установленный Rust):
```bash
cargo install websocat
```

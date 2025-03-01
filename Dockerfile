FROM python:3.9-slim
WORKDIR /chat_app
COPY requirements.txt .
COPY pytest.ini /chat_app/pytest.ini
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
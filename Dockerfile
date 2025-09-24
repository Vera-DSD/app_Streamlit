FROM python:3.10-slim

WORKDIR /app

# Обновляем pip и устанавливаем зависимости с ретраями
RUN pip install --upgrade pip

COPY requirements.txt .

# Пробуем разные зеркала PyPI с ретраями
RUN pip install --no-cache-dir --retries 3 --timeout 60 -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "my_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

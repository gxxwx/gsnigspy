# Используем стабильную версию Python 3.11
FROM python:3.11-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Запуск бота
CMD ["python", "bot.py"]

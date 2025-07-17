# Используем официальный образ Python
FROM python:3.13

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Установка переменных окружения (если нужно)
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Команда, которая запускается при старте контейнера
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
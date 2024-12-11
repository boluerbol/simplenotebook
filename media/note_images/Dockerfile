# Используем официальный Python-образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=notebook_project.settings

# Создаем папку для медиафайлов
RUN mkdir -p /app/media

# Открываем порт для Django
EXPOSE 8000

# Запуск команды для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

   # Используйте официальный образ Python в качестве базового
   FROM python:3.11

   # Устанавливаем рабочую директорию для нашего проекта
   WORKDIR /app

   # Копируем файл зависимостей в контейнер
   COPY requirements.txt .

   RUN apt update

   RUN apt install -y postgresql-client

   RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       apache2 \
       libapache2-mod-wsgi-py3 \
       build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

   # Устанавливаем зависимости
   RUN pip install --no-cache-dir -r requirements.txt

   # Копируем весь оставшийся проектный код в рабочую директорию контейнера
   COPY . .

   COPY apache-django.conf /etc/apache2/sites-available/000-default.conf
   RUN a2enmod wsgi

   # Экспорт переменной окружения для корректного запуска Django
   ENV PYTHONUNBUFFERED=1
   RUN python manage.py collectstatic --noinput

   # Открываем порт, который будет использоваться сервером приложения
   EXPOSE 80

   # Команда для запуска сервера разработки Django. Замените `<project_name>` на имя вашего проекта.
   CMD ["apache2ctl", "-D", "FOREGROUND"]
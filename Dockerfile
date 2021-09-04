FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/pikabu_clone

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt
RUN pip install django_extensions
RUN pip install django-cors-headers

COPY . /usr/src/pikabu_clone

# EXPOSE 8000

# CMD ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker-compose build
# docker-compose up -d
# docker-compose exec web python manage.py migrate --noinput
# docker-compose down -v  // or ctrl+C if not deamon
# VIDEOFLIX - Django Backend

This is a scalable video processing backend built with Django and containerized using Docker. It supports video uploads, automatic transcoding into multiple resolutions via background tasks, user authentication with email verification, and performance optimization through Redis-based caching.

---

## Features

- Video upload API
- Automatic transcoding to multiple resolutions using `ffmpeg`
- Background task execution with **Django RQ** and **Redis**
- User registration with **email verification**
- Caching layer implemented with **django-redis**
- Fully containerized using **Docker** and **Docker Compose**
- Environment-based configuration via `.env` file

---

## Tech Stack

- **Framework:** Django 5, Django REST Framework
- **Task Queue:** Django RQ + Redis
- **Video Processing:** ffmpeg via `ffmpeg-python`
- **Database:** PostgreSQL 15
- **Web Server:** Gunicorn
- **Deployment:** Docker & Docker Compose

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

```bash
bash
KopierenBearbeiten
docker-compose up --build

```

### Available Services

| Service | URL / Port |
| --- | --- |
| Django Web | localhost:8081 |
| PostgreSQL | localhost:5430 |
| Redis | internal (6379) |

---

## Project Structure

```
bash
KopierenBearbeiten
.
├── backend/              # Django project code
├── media/                # Uploaded video files
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── .env

```

---

## Environment Configuration

Create a `.env` file with the following sample content:

```
env
KopierenBearbeiten
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
DATABASE_URL=postgres://postgres:yourpassword@db:5432/postgres
REDIS_URL=redis://redis:6379/0

EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_USE_TLS=True

```

---

## Docker Overview

### `docker-compose.yml`

Defines the following services:

- **web**: Django app served via Gunicorn, with automatic database migrations on startup
- **rqworker**: Background task worker
- **db**: PostgreSQL 15 database
- **redis**: Redis 7 for caching and queue management

---

## User Registration & Email Verification

1. Users register via the provided API.
2. A verification email is sent with an activation link.
3. Upon clicking the link, the user account is activated.

> Ensure SMTP credentials are correctly configured in the .env file.
> 

---

## Key Dependencies

- `Django`, `djangorestframework`: Core web and API framework
- `ffmpeg-python`: Interface for video transcoding
- `django-rq`: Queue integration for background tasks
- `django-redis`: Redis caching backend
- `gunicorn`: Production WSGI server
- `psycopg2-binary`: PostgreSQL adapter

---

## Common Commands

### Run Migrations

```bash
bash
python manage.py makemigrations
python manage.py migrate

```

### Create Superuser

```bash
bash
python manage.py createsuperuser

```

### Start Worker (manually, if needed)

```bash
bash
docker-compose run rqworker

```

### Connect to the Database

```bash
psql -h localhost -p 5430 -U postgres

```

---

## Security Notes for Production

- Set `DEBUG=0` in production environments
- Use a strong `SECRET_KEY`
- Define correct `ALLOWED_HOSTS`
- Use HTTPS and a reverse proxy like Nginx
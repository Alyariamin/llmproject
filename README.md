# 🚀 Django + Redis + Celery + Docker Project

This project is a Dockerized Django backend using:

- Django
- Redis
- Celery
- SQLite (development)
- OpenRouter API
- Docker & Docker Compose

---

## 📦 Requirements

- Docker
- Docker Compose

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
OPENROUTER_API_KEY=your_openrouter_api_key
REDIS_HOST=redis
```

⚠️ Do NOT commit your `.env` file.

---

## 🐳 Run with Docker

Build and start all services:

```bash
docker compose up --build
```

The app will be available at:

```
http://localhost:8000
```

---

## 🗄 Run Migrations

If migrations are not automatic:

```bash
docker compose exec web python manage.py migrate
```

---

## 🛑 Stop the Project

```bash
docker compose down
```

---

## 🧱 Services

The project runs 3 containers:

- `web` → Django app
- `redis` → Redis server
- `celery` → Celery worker

---

## 🧠 Tech Stack

- Django
- Celery
- Redis
- Docker
- SQLite
---

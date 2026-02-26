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


## 👤 Create Superuser for Admin Panel

To access Django admin:

```bash
docker compose exec web python manage.py createsuperuser
```
---


- Admin panel URL: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Search URL: [http://localhost:8000/search/](http://localhost:8000/search/)

---
## 🔍 Search API

You can send POST requests to the search endpoint:

```
http://localhost:8000/search/
```

### Request Format (JSON)

```json
{
  "question": "my question"
}
```

### Example using `curl`

```bash
curl -X POST http://localhost:8000/search/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Django?"}'
```

The response will contain the answer returned by the OpenRouter API (via your backend logic).

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

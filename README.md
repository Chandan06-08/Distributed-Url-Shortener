# Distributed URL Shortener

A production-inspired URL Shortener built with **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**. The application generates short URLs, redirects users efficiently, tracks analytics, supports URL expiration, and uses Redis caching to reduce database lookups.

---

## Features

* Generate unique short URLs
* Redirect users to the original URL
* Store URLs permanently in PostgreSQL
* Track click analytics
* Redis caching for faster redirects
* URL expiration support
* Database schema versioning using Alembic
* Dockerized Redis
* RESTful API built with FastAPI

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* Alembic

### Cache

* Redis

### DevOps & Tools

* Docker
* Git
* GitHub
* python-dotenv

---

## Project Structure

```
Distributed-Url-Shortener/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── cache.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## Architecture

```
                Client
                   │
                   ▼
              FastAPI API
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
    Redis Cache         PostgreSQL
        │                     │
        └──────────┬──────────┘
                   ▼
          Permanent URL Storage
```

---

## API Endpoints

### Create Short URL

**POST**

```
/shorten
```

Example Request

```json
{
    "url": "https://youtube.com",
    "expires_in_days": 7
}
```

Example Response

```json
{
    "short_code": "mk4Esn"
}
```

If `expires_in_days` is omitted, the URL never expires.

---

### Redirect URL

**GET**

```
/{short_code}
```

Example

```
GET /mk4Esn
```

Behavior

* Redirects to the original URL.
* Increments click count.
* Uses Redis cache for faster retrieval.
* Returns **410 Gone** if the URL has expired.
* Returns **404 Not Found** if the short code does not exist.

---

## Database Schema

### urls

| Column       | Type                 |
| ------------ | -------------------- |
| id           | BIGINT               |
| short_code   | VARCHAR(10)          |
| original_url | TEXT                 |
| click_count  | BIGINT               |
| created_at   | TIMESTAMP            |
| expires_at   | TIMESTAMP (Nullable) |

---

## Redis Caching

Redis stores frequently accessed URLs to reduce database queries.

### First Request

```
Client
   │
Redis (Miss)
   │
PostgreSQL
   │
Redis Cache Updated
   │
Redirect
```

### Subsequent Requests

```
Client
   │
Redis (Hit)
   │
Redirect
```

---

## URL Expiration

Users can optionally specify an expiration period while creating a short URL.

Example

```json
{
    "url": "https://youtube.com",
    "expires_in_days": 7
}
```

The backend converts this into an absolute timestamp (`expires_at`) and stores it in PostgreSQL.

Expired URLs return:

```
410 Gone
```

---

## Click Analytics

Each successful redirect increments the corresponding URL's click count stored in PostgreSQL.

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/Chandan06-08/Distributed-Url-Shortener.git

cd Distributed-Url-Shortener
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file.

```
DATABASE_URL=your_postgresql_connection_string
```

### Start Redis

```bash
docker run -d --name redis-server -p 6379:6379 redis
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start Server

```bash
uvicorn app.main:app --reload
```

---

## Future Improvements

* JWT Authentication
* Rate Limiting using Redis
* Background Jobs for Analytics
* Docker Compose
* CI/CD with GitHub Actions
* User Accounts
* Custom Domains
* URL Analytics Dashboard
* Distributed Cache Synchronization
* Load Testing
* Cloud Deployment

---

## Author

**Chandan Yadav**

GitHub: https://github.com/Chandan06-08

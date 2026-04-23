# hng14-stage2-devops

A simple job processing system built with FastAPI, Redis, a Python worker, and an Express frontend.

## Architecture

```
frontend (Express + HTML)  →  api (FastAPI)  →  redis  ←  worker (Python)
        :3000                     :8000            :6379
```

- **Frontend** — Express server serving a static HTML UI. Submits jobs and polls for status.
- **API** — FastAPI app that creates jobs, pushes them to Redis, and exposes a status endpoint.
- **Worker** — Python process that consumes jobs from Redis and processes them.
- **Redis** — Queue and job state store.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (recommended)
- Or: Python 3.11+, Node.js 18+, and a running Redis instance

---

## Running with Docker (recommended)

```bash
docker compose up --build
```

That's it. All four services start together.

| Service  | URL                    |
|----------|------------------------|
| Frontend | http://localhost:3000  |
| API      | http://localhost:8000  |
| API Docs | http://localhost:8000/docs |

To stop:

```bash
docker compose down
```

---

## Running Locally (without Docker)

You'll need four terminals.

### 1. Start Redis

If you have Docker:

```bash
docker run -d -p 6379:6379 redis
```

### 2. Start the API

```bash
cd api
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
# or
source .venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Start the Worker

```bash
cd worker
source .venv/Scripts/activate  # Windows Git Bash
# or
source .venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
python worker.py
```

### 4. Start the Frontend

```bash
cd frontend
npm install
node app.js
```

Then open http://localhost:3000 in your browser.

---

## Environment Variables

Each service has its own `.env` file.

**`api/.env`**
```env
REDIS_HOST=localhost
```

**`worker/.env`**
```env
REDIS_HOST=localhost
```

**`frontend/.env`**
```env
API_URL=http://localhost:8000
PORT=3000
```

> When running via Docker, `REDIS_HOST` should be `redis` and `API_URL` should be `http://api:8000`. These are already handled in `docker-compose.yml`.

---

## Project Structure

```
stage-2-devops/
├── api/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── app.js
│   ├── views/
│   │   └── index.html
│   ├── package.json
│   ├── Dockerfile
│   └── .env
├── worker/
│   ├── worker.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── docker-compose.yml
├── FIXES.md
└── README.md
```
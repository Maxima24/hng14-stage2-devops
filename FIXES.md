# FIXES.md

## 1. FastAPI — Typo in Redis Host
**Problem:** Redis host was `"localh\`ost"` with a backtick inside the string, causing a connection error.  
**Fix:** Corrected to `"localhost"`.

```python
r = redis.Redis(host="localhost", port=6379)
```

---

## 2. FastAPI — Redis Host Not Configurable via Env
**Problem:** Redis host was hardcoded to `localhost`, which breaks inside Docker where the Redis service is reachable via its service name.  
**Fix:** Used `os.getenv` to read from environment variables.

```python
import os
r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)
```

---

## 3. Express Frontend — Env Vars Returning Undefined
**Problem:** `process.env.API_URL` and `process.env.PORT` were `undefined` because the `.env` file was never loaded.  
**Fix:** Added `dotenv` at the very top of `app.js`.

```javascript
import * as dotenv from 'dotenv';
dotenv.config();
```

---

## 4. Express Frontend — `__dirname` Not Defined
**Problem:** `ReferenceError: __dirname is not defined in ES module scope` when serving static files.  
**Fix:** Reconstructed `__dirname` manually for ES modules.

```javascript
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

---

## 5. Express Frontend — CORS Not Enabled
**Problem:** Browser blocked requests from the HTML frontend to the Express API.  
**Fix:** Added `cors` middleware.

```javascript
import cors from 'cors';
app.use(cors());
```

---

## 6. HTML Frontend — Fetching Wrong Port
**Problem:** `fetch('/submit')` was hitting Live Server on port `8080` instead of the Express app.  
**Fix:** Hardcoded `API_URL` in the HTML to point to the Express server.

```javascript
const API_URL = 'http://localhost:3000';
```

---

## 7. HTML Frontend — No Error Handling
**Problem:** When `job_id` was undefined, `substring` threw an uncaught error and crashed the poll loop.  
**Fix:** Added try/catch to `submitJob` and `pollJob`, with a guard on `job_id` before polling.

```javascript
if (!data.job_id) {
  document.getElementById('result').innerText = `Error: ${data.error || 'No job_id returned'}`;
  return;
}
```

---

## 8. Worker — Not Running
**Problem:** Jobs were stuck in `queued` status forever because nothing was consuming the Redis queue.  
**Fix:** Created `worker.py` as a separate process that picks up jobs via `brpop`, updates status to `processing`, simulates work, then marks as `completed`.

```python
while True:
    job = r.brpop("job", timeout=5)
    if job:
        job_id = job[1].decode()
        r.hset(f"job:{job_id}", "status", "processing")
        time.sleep(3)
        r.hset(f"job:{job_id}", "status", "completed")
```

---

## 9. Docker — Services Not Wired Correctly
**Problem:** No Dockerfiles or `docker-compose.yml` existed. Services couldn't be orchestrated together.  
**Fix:** Created `Dockerfile` for `api`, `frontend`, and `worker`, and a `docker-compose.yml` wiring all four services (redis, api, worker, frontend) with `env_file`, `depends_on`, and healthchecks.

---

## 10. Docker — `localhost` Breaks Inter-Service Communication
**Problem:** Inside Docker, services can't reach each other via `localhost`. Redis would be unreachable from the api and worker containers.  
**Fix:** Updated `.env` files to use Docker service names instead.

```env
# api/.env and worker/.env
REDIS_HOST=redis

# frontend/.env
API_URL=http://api:8000
```
import redis
import time

r = redis.Redis(host="localhost", port=6379)

print("Worker started, waiting for jobs...")

while True:
    job = r.brpop("job", timeout=5)
    if job:
        job_id = job[1].decode()
        print(f"Processing job: {job_id}")
        
        r.hset(f"job:{job_id}", "status", "processing")
        time.sleep(3)  # simulate work
        r.hset(f"job:{job_id}", "status", "completed")
        
        print(f"Completed job: {job_id}")
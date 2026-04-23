#!/bin/bash
set -e

MAX_WAIT=60
INTERVAL=3

echo "Submitting job..."
RESPONSE=$(curl -sf -X POST http://localhost:3000/submit)
JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

elapsed=0
while [ $elapsed -lt $MAX_WAIT ]; do
  STATUS=$(curl -sf http://localhost:3000/status/$JOB_ID | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Job completed successfully"
    exit 0
  fi
  sleep $INTERVAL
  elapsed=$((elapsed + INTERVAL))
done

echo "Job did not complete within ${MAX_WAIT}s"
exit 1
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch("redis.Redis") as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)


@pytest.fixture
def mock_redis():
    with patch("main.r") as redis_mock:
        yield redis_mock


def test_create_job_returns_job_id(mock_redis):
    """POST /jobs should return a valid job_id"""
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0


def test_create_job_pushes_to_redis(mock_redis):
    """POST /jobs should push job to Redis queue and set status"""
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")
    data = response.json()
    job_id = data["job_id"]

    mock_redis.lpush.assert_called_once_with("job", job_id)
    mock_redis.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")


def test_get_job_returns_status(mock_redis):
    """GET /jobs/{job_id} should return job status"""
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-job-123")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"


def test_get_job_not_found(mock_redis):
    """GET /jobs/{job_id} should return error when job doesn't exist"""
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-job")

    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"


def test_health_check():
    """GET /health should return ok status"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job_id_is_unique(mock_redis):
    """Each POST /jobs should return a different job_id"""
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response1 = client.post("/jobs")
    response2 = client.post("/jobs")

    assert response1.json()["job_id"] != response2.json()["job_id"]

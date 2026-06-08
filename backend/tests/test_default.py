"""Default test."""

from fastapi.testclient import TestClient

import api

client = TestClient(api.app)

OKAY: int = 200


def test_health_check() -> None:
    """Test health check endpoint."""
    response = client.get("/")
    result = response.json()
    assert response.status_code == OKAY
    assert result == {"status": "ok", "user_agent": "testclient", "api_env": "development"}

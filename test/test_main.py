from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK, "Health check endpoint should return 200 OK"
    assert response.json() == {"status": "ok"}, "Health check endpoint should return the correct status message"
    
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

user_id = str(uuid.uuid4())


def test_create_user():
    sample_payload = {
        "name": "PLACEHOLDER",
        "surname": "PLACEHOLDER",
        "email": "john.doe@example.com",
        "password": "PLACEHOLDER",
    }
    response = client.post("/api/users", json=sample_payload)
    assert response.status_code == 201
    assert response.json() == {
        "user_id": user_id,
        "name": "PLACEHOLDER",
        "surname": "PLACEHOLDER",
        "email": "john.doe@example.com",
        "is_active": True,
    }

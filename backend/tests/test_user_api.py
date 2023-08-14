import json
import pytest


@pytest.mark.asyncio
async def test_root(client):
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}


@pytest.mark.asyncio
async def test_create_user(client):
    sample_payload = {
        "name": "PLACEHOLDER",
        "surname": "PLACEHOLDER",
        "email": "user6@example.com",
        "password": "PLACEHOLDER",
    }
    response = client.post("/api/users", data=json.dumps(sample_payload))
    data_from_resp = response.json()
    assert response.status_code == 201
    assert data_from_resp["name"] == sample_payload["name"]
    assert data_from_resp["surname"] == sample_payload["surname"]
    assert data_from_resp["email"] == sample_payload["email"]
    assert data_from_resp["is_active"] is True

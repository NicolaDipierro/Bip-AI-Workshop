from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "UP"
    }


def test_create_order():

    payload = {
        "customer": "Mario Rossi",
        "quantity": 5
    }

    response = client.post(
        "/orders",
        json=payload
    )

    assert response.status_code == 200
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_chat_contract():
    response = client.post("/v1/chat", json={
        "message": "Explain backpropagation",
        "mode": "learn",
        "student": {
            "branch": "CSE",
            "semester": 5,
            "known_skills": ["Python"]
        }
    })
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "learn"
    assert len(body["next_steps"]) == 3

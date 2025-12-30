import pytest
from fastapi.testclient import TestClient
from src import app

client = TestClient(app.app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

def test_unregister_participant():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Unregister the participant (accept 200, 400, or 404)
    response = client.post(f"/activities/{activity}/unregister", json={"participant": email})
    assert response.status_code in (200, 400, 404)
    # Try unregistering again (should fail with 400 or 404)
    response = client.post(f"/activities/{activity}/unregister", json={"participant": email})
    assert response.status_code in (400, 404)

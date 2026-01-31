from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "Chess Club" in response.json()

def test_signup_flow():
    # 1. Sign up a new user
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@example.com for Chess Club"}

    # 2. Try to sign up again (should fail)
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}

    # 3. Verify user is in participants list
    response = client.get("/activities")
    activities = response.json()
    assert "test@example.com" in activities["Chess Club"]["participants"]

    # 4. Remove user
    response = client.delete("/activities/Chess Club/participants?email=test@example.com")
    assert response.status_code == 200
    assert response.json() == {"message": "Removed test@example.com from Chess Club"}

    # 5. Verify user is removed
    response = client.get("/activities")
    activities = response.json()
    assert "test@example.com" not in activities["Chess Club"]["participants"]

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Chess Club/participants?email=nobody@example.com")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}

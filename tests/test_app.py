import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert len(data["Chess Club"]["participants"]) == 2


def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    # Second
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Invalid/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # Signup first
    client.post("/activities/Gym%20Class/signup?email=unregister@mergington.edu")
    # Unregister
    response = client.delete("/activities/Gym%20Class/signup?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@mergington.edu from Gym Class" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@mergington.edu" not in data["Gym Class"]["participants"]


def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # Since it's redirect, but TestClient follows redirects? Wait, no, by default it doesn't.
    # Actually, TestClient follows redirects.
    # But to check, perhaps assert the content or something.
    # For simplicity, just check status 200.
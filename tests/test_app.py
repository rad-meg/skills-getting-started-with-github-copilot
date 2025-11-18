import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up testuser@mergington.edu for Chess Club"


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity():
    response = client.delete("/activities/Chess Club/unregister", params={"email": "michael@mergington.edu"})
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_from_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonexistent_participant():
    response = client.delete("/activities/Chess Club/unregister", params={"email": "nonexistent@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
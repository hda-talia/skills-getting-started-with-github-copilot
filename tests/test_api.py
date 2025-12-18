from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_and_unregister_flow():
    activity = "Soccer Team"
    email = "tester@example.com"

    # Ensure activity exists and starts empty for this test
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert activity in activities
    assert isinstance(activities[activity]["participants"], list)

    # Ensure email not present initially
    assert email not in activities[activity]["participants"]

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    data = resp.json()
    assert "Signed up" in data["message"]

    # Verify participant added
    resp = client.get("/activities")
    activities = resp.json()
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    data = resp.json()
    assert "Unregistered" in data["message"]

    # Verify participant removed
    resp = client.get("/activities")
    activities = resp.json()
    assert email not in activities[activity]["participants"]

import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    email = "new-student@example.com"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/Chess Club/signup?email={email}")
    assert unregister_response.status_code == 200

    payload = unregister_response.json()
    assert "Removed" in payload["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]

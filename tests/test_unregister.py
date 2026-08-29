from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    unregister_response = client.delete(endpoint)
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/participants?email=student@mergington.edu"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_enrolled_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422

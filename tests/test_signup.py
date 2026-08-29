from urllib.parse import quote


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "alex@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    signup_response = client.post(endpoint)
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_returns_400_for_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown%20Club/signup?email=student@mergington.edu"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_422_when_email_is_missing(client):
    # Arrange
    endpoint = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422


def test_signup_handles_encoded_activity_name(client):
    # Arrange
    activity_name = "Science Olympiad"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

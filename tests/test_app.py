
import sqlite3
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    # Create a separate temporary database for testing
    database = tmp_path / "test_submissions.db"

    app = create_app({
        "TESTING": True,
        "DATABASE": str(database)
    })

    with app.test_client() as client:
        yield client


def get_submissions(database):
    connection = sqlite3.connect(database)
    result = connection.execute(
        "SELECT * FROM submissions"
    ).fetchall()
    connection.close()
    return result


def test_valid_submission_is_saved_and_displayed(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration_number": "FA23-BAI-050",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://github.com"
    })

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert b"Ali Khan" in response.data
    assert b"FA23-BAI-050" in response.data

    with client.application.app_context():
        database = client.application.config["DATABASE"]

    submissions = get_submissions(database)

    assert len(submissions) == 1
    assert submissions[0][1] == "Ali Khan"


def test_missing_registration_number_is_rejected(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration_number": "",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://github.com"
    })

    assert response.status_code == 200
    assert b"All fields are required." in response.data

    with client.application.app_context():
        database = client.application.config["DATABASE"]

    submissions = get_submissions(database)

    assert len(submissions) == 0


def test_invalid_submission_url_is_rejected(client):
    response = client.post("/", data={
        "name": "Ali Khan",
        "registration_number": "FA23-BAI-050",
        "assignment_title": "DevOps Lab",
        "submission_url": "abc123"
    })

    assert response.status_code == 200
    assert b"Please enter a valid submission URL." in response.data

    with client.application.app_context():
        database = client.application.config["DATABASE"]

    submissions = get_submissions(database)

    assert len(submissions) == 0

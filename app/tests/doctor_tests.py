from fastapi.testclient import TestClient
import pytest

from app.settings import Settings


@pytest.fixture(autouse=True, params=[True, False])
def mode(request) -> None:
    """
    Run all the tests in this file in both in_database and in_memory mode.
    """
    Settings.in_database = request.param


def test_get_all_doctors(client: TestClient):
    # Test that getting all doctors truly gets them all
    rv = client.get('/doctors')
    assert rv.status_code == 200

    # Can't guarantee order, so test that we get the expected count and fields seem to make sense
    data = rv.json()
    assert len(data) == 2
    for field in ['id', 'first_name', 'last_name']:
        assert field in data[0]


def test_get_valid_doctor(client: TestClient):
    # Test getting a single doctor, successfully

    rv = client.get('/doctors/0')
    assert rv.status_code == 200

    data = rv.json()
    assert data['id'] == 0
    assert data['first_name'] == 'Jane'
    assert data['last_name'] == 'Wright'


def test_get_invalid_doctor(client: TestClient):
    # Test getting a single doctor that doesn't exist
    rv = client.get('/doctors/2')
    assert rv.status_code == 404


def test_create_doctor(client: TestClient):
    # Test creating a real doctor, successfully

    rv = client.post(
        '/doctors',
        json=(dict(first_name='Gregory', last_name='House'))
    )

    assert rv.status_code == 200

    data = rv.json()
    assert data['id'] == 2

import pytest
from app.app import create_app
from fastapi.testclient import TestClient
from app.database.db import DB

from app.settings import Settings


@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app()
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """
    Reset the database between tests
    """
    if Settings.in_database:
        DB.init_db()
        DB.seed()

    yield

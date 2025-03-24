import pytest
from unittest.mock import MagicMock, create_autospec
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session
from app.db.utils import get_db

# Create a mock session
@pytest.fixture
def mock_db():
    mock_session = create_autospec(Session)
    return mock_session

@pytest.fixture
def client(mock_db):
    # Override the dependency
    app.dependency_overrides[get_db] = lambda: mock_db
    test_client = TestClient(app)
    yield test_client
    # Clean up after tests
    app.dependency_overrides.clear()

@pytest.fixture
def mock_db_query(mock_db):
    """
    Fixture to mock database queries.
    Usage: mock_db_query.return_value.filter.return_value.first.return_value = your_mock_data
    """
    mock_query = MagicMock()
    mock_db.query = mock_query
    return mock_query

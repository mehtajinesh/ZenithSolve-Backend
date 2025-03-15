from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import db


client = TestClient(app)


def test_read_root(db):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

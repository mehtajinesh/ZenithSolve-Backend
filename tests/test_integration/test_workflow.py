# tests/test_integration/test_workflow.py
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session
from tests.conftest import db

client = TestClient(app)

# Mock the database session
def test_full_workflow(db: Session):
    # Create a category
    category_response = client.post("/categories/", json={"name": "Test Category"})
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    # Create a problem
    problem_response = client.post("/problems/", json={
        "title": "Test Problem",
        "statement": "Test Statement",
        "constraints": "Test Constraints",
        "examples": "Test Examples",
        "category_id": category_id
    })
    assert problem_response.status_code == 200
    problem_id = problem_response.json()["id"]

    # Create a real world example
    example_response = client.post("/real_world_examples/", json={
        "description": "Test Description",
        "business_impact": "Test Impact",
        "consequences": "Test Consequences",
        "problem_id": problem_id
    })
    assert example_response.status_code == 200
    example_id = example_response.json()["id"]

    # Create a solution
    solution_response = client.post("/solutions/", json={
        "language": "Python",
        "code": "print('Hello, World!')",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "problem_id": problem_id
    })
    assert solution_response.status_code == 200
    solution_id = solution_response.json()["id"]

    # Retrieve the problem with related examples and solutions
    problem_retrieve_response = client.get(f"/problems/{problem_id}")
    assert problem_retrieve_response.status_code == 200
    problem_data = problem_retrieve_response.json()
    assert problem_data["id"] == problem_id
    assert len(problem_data["real_world_examples"]) == 1
    assert len(problem_data["solutions"]) == 1
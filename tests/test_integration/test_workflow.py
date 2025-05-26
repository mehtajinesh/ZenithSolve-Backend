from fastapi.testclient import TestClient
from app.schemas.problems import ProblemIn
from app.schemas.categories import Category
import uuid
from unittest.mock import MagicMock, ANY

# Test complete workflow of creating a category and a problem, then retrieving them
def test_workflow(client: TestClient, mock_db):
    # Step 1: Create a new category
    unique_category_name = f"Test Category {uuid.uuid4()}"
    category_in = Category(name=unique_category_name)
    category_id = 1  # Using integer ID

    # Setup mock behavior for category operations
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing category
    mock_category = MagicMock()
    mock_category.id = category_id
    mock_category.name = unique_category_name
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', category_id)

    created_category = client.post("/categories/", json=category_in.dict())
    
    assert created_category.status_code == 201
    created_category_json = created_category.json()
    assert created_category_json["name"] == unique_category_name

    # Step 2: Create a new problem associated with the created category
    unique_problem_slug = f"test-problem-{uuid.uuid4()}"
    problem_id = 1  # Using integer ID
    
    # Create problem using the schema
    example = "Input: [1, 2] Output: 3 Explanation: 1 + 2 = 3"
    problem_in = ProblemIn(
        title="Test Problem",
        slug_id=unique_problem_slug,
        difficulty="Medium",
        description="Test Description",
        examples=[example],
        categories=[unique_category_name]
    )

    # Setup mock behavior for problem operations
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing problem
    # add mock category to the problem
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_category]
    mock_problem = MagicMock()
    mock_problem.id = problem_id
    mock_problem.title = problem_in.title
    mock_problem.slug_id = problem_in.slug_id
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', problem_id)
    
    created_problem = client.post("/problems/", json=problem_in.dict())
    
    assert created_problem.status_code == 201
    created_problem_json = created_problem.json()
    assert created_problem_json["title"] == "Test Problem"
    assert created_problem_json["slug_id"] == unique_problem_slug
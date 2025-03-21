# tests/test_crud/test_problems.py
import uuid
from app.schemas.problems import ProblemIn, ExampleItem
from app.db.models.problem import Problem
from app.crud import problems
import pytest
from unittest.mock import MagicMock

def test_create_problem_existing(mock_db):
    # Mock existing problem
    unique_slug = f"test-problem-{uuid.uuid4()}"
    mock_existing_problem = Problem(
        title="Existing Problem",
        slug_id=unique_slug,
        difficulty="Medium",
        description="Existing Description",
        examples=[
            ExampleItem(input="[1, 2]", output="3", explanation="1 + 2 = 3")
        ],
        id=1
    )
    
    # Setup mock behavior for existing problem
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_problem
    
    # Attempt to create a problem that already exists
    problem_in = ProblemIn(
        title="Existing Problem",
        slug_id=unique_slug,
        difficulty="Medium",
        description="Existing Description",
        examples=[
            ExampleItem(input="[1, 2]", output="3", explanation="1 + 2 = 3")
        ],
        categories=["Test Category"]
    )
    
    with pytest.raises(ValueError, match=f"Problem with slug_id '{unique_slug}' already exists"):
        problems.create_problem(db=mock_db, problem=problem_in)


def test_create_problem_category_not_exist(mock_db):
    # Mock behavior for category not found
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Attempt to create a problem with a non-existent category
    problem_in = ProblemIn(
        title="New Problem",
        slug_id=f"test-problem-{uuid.uuid4()}",
        difficulty="Medium",
        description="New Description",
        examples=[
            ExampleItem(input="[1, 2]", output="3", explanation="1 + 2 = 3")
        ],
        categories=["NonExistentCategory"]
    )
    
    with pytest.raises(ValueError, match="One or more categories do not exist."):
        problems.create_problem(db=mock_db, problem=problem_in)


def test_create_problem_new(mock_db):
    # Mock behavior for new category
    mock_category = MagicMock()
    mock_category.name = "Test Category"
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Setup mock behavior for adding a new category
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_category]
    
    # Create a new problem
    problem_in = ProblemIn(
        title="New Problem",
        slug_id=f"test-problem-{uuid.uuid4()}",
        difficulty="Medium",
        description="New Description",
        examples=[
            ExampleItem(input="[1, 2]", output="3", explanation="1 + 2 = 3")
        ],
        categories=["Test Category"]
    )
    
    # Mock the behavior of adding and committing to the database
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    created_problem = problems.create_problem(db=mock_db, problem=problem_in)
    
    # Check that the problem was created correctly
    assert created_problem.slug_id == problem_in.slug_id
    assert created_problem.title == problem_in.title
    assert created_problem.difficulty == problem_in.difficulty
    assert created_problem.description == problem_in.description
    assert created_problem.examples == problem_in.examples
    assert "Test Category" in created_problem.categories
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_get_problem_existing(mock_db):
    # Mock existing problem
    unique_slug = f"test-problem-{uuid.uuid4()}"
    mock_problem = Problem(
        title="Existing Problem",
        slug_id=unique_slug,
        difficulty="Medium",
        description="Existing Description",
        examples='[{"input": "[1, 2]","output": "3","explanation": "1 + 2 = 3"}]',
        solution_approach = "",
        best_time_complexity = "NA",
        best_space_complexity = "NA",
        real_world_examples=[],
        solutions = [],
        id=1
    )
    
    # Setup mock behavior for existing problem
    mock_db.query.return_value.filter.return_value.first.return_value = mock_problem
    
    # Retrieve the problem
    retrieved_problem = problems.get_problem(db=mock_db, slug_id=unique_slug)
    
    # Check that the retrieved problem matches the mock
    assert retrieved_problem.slug_id == unique_slug
    assert retrieved_problem.title == "Existing Problem"
    assert retrieved_problem.difficulty == "Medium"
    assert retrieved_problem.description == "Existing Description"
    assert len(retrieved_problem.examples) == 1
    assert retrieved_problem.examples[0].input == "[1, 2]"
# tests/test_crud/test_problems.py
import uuid
from app.schemas.problems import ProblemIn
from app.db.models.problem import Problem
from app.db.models.category import Category
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
            "[1, 2]", "3", "1 + 2 = 3"
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
            "[1, 2]", "3", "1 + 2 = 3"
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
            "[1, 2]", "3", "1 + 2 = 3"
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
            "[1, 2]", "3", "1 + 2 = 3"
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
        id=1,
        slug_id=unique_slug,
        title="Existing Problem",
        difficulty="Medium",
        description="Existing Description",
        clarifying_questions = ["Sample Question"],
        categories=[Category(name="Test Category")],
        constraints="1 <= input <= 100",
        examples=["Input: [1, 2] Output: 3 Explanation: 1 + 2 = 3"],
        best_time_complexity = "NA",
        best_space_complexity = "NA",
        real_world_examples=[],
        solutions = [],
    )
    
    # Setup mock behavior for existing problem
    mock_db.query.return_value.filter.return_value.first.return_value = mock_problem
    
    # Retrieve the problem
    retrieved_problem = problems.get_problem(db=mock_db, slug_id=unique_slug)
    
    # Check that the retrieved problem matches the mock
    assert retrieved_problem.slug_id == unique_slug
    assert retrieved_problem.title == "Existing Problem"
    assert retrieved_problem.difficulty == "Medium"
    assert retrieved_problem.constraints == "1 <= input <= 100"
    assert retrieved_problem.best_time_complexity == "NA"
    assert retrieved_problem.best_space_complexity == "NA"
    assert retrieved_problem.solutions == []
    assert retrieved_problem.clarifying_questions == ["Sample Question"]
    assert retrieved_problem.description == "Existing Description"
    assert len(retrieved_problem.examples) == 1
    assert retrieved_problem.examples[0] == "Input: [1, 2] Output: 3 Explanation: 1 + 2 = 3"

def test_get_problem_not_found(mock_db):
    # Mock behavior for non-existent problem
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Retrieve a non-existent problem
    with pytest.raises(ValueError, match="Problem with slug_id 'non-existent' not found."):
        problems.get_problem(db=mock_db, slug_id="non-existent")


def test_update_problem_success(mock_db):
    # Mock existing problem
    unique_slug = f"test-problem-{uuid.uuid4()}"
    mock_problem = Problem(
        id=1,
        slug_id=unique_slug,
        title="Original Title",
        difficulty="Medium",
        description="Original Description",
        categories=[Category(name="Test Category")],
        constraints="1 <= input <= 100",
        examples=["Input: [1, 2] Output: 3 Explanation: 1 + 2 = 3"],
        best_time_complexity="NA",
        best_space_complexity="NA",
        real_world_examples=[],
        solutions=[],
    )
    
    # Setup mock behavior
    mock_db.query.return_value.filter.return_value.first.return_value = mock_problem
    mock_category = MagicMock()
    mock_category.name = "New Category"
    mock_db.query.return_value.filter.return_value.all.return_value = [mock_category]
    
    # Update problem
    updated_problem_in = ProblemIn(
        slug_id=unique_slug,
        title="Updated Title",
        difficulty="Hard",
        description="Updated Description",
        constraints="1 <= input <= 200",
        examples=[
            "Input: [3, 4] Output: 7 Explanation: 3 + 4 = 7"
        ],
        categories=["New Category"]
    )
    
    result = problems.update_problem(db=mock_db, problem_id=unique_slug, problem_update=updated_problem_in)
    
    # Check that updated values are reflected
    assert result["slug_id"] == unique_slug
    assert result["title"] == "Updated Title"
    assert result["difficulty"] == "Hard"
    assert result["description"] == "Updated Description"
    assert result["constraints"] == "1 <= input <= 200"
    assert "New Category" in result["categories"]
    mock_db.commit.assert_called_once()


def test_update_problem_not_found(mock_db):
    # Mock behavior for non-existent problem
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Try to update a non-existent problem
    problem_update = ProblemIn(
        slug_id="non-existent",
        title="Updated Title",
        difficulty="Hard",
        description="Updated Description",
        examples=[],
        categories=[]
    )
    
    with pytest.raises(ValueError, match="Problem with slug_id 'non-existent' not found."):
        problems.update_problem(db=mock_db, problem_id="non-existent", problem_update=problem_update)


def test_update_problem_new_slug_exists(mock_db):
    # Mock existing problem
    original_slug = f"original-slug-{uuid.uuid4()}"
    new_slug = f"new-slug-{uuid.uuid4()}"
    
    mock_problem = Problem(
        id=1,
        slug_id=original_slug,
        title="Original Title",
        difficulty="Medium",
        description="Original Description"
    )
    
    mock_existing_problem_with_new_slug = Problem(
        id=2,
        slug_id=new_slug,
        title="Another Problem"
    )
    
    # Setup mock behavior - first call is for the original problem, second is for checking if new slug exists
    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_problem, mock_existing_problem_with_new_slug]
    
    # Try to update with a slug that already exists
    problem_update = ProblemIn(
        slug_id=new_slug,
        title="Updated Title",
        difficulty="Hard",
        description="Updated Description",
        examples=[],
        categories=[]
    )
    
    with pytest.raises(ValueError, match=f"Problem with slug_id '{new_slug}' already exists."):
        problems.update_problem(db=mock_db, problem_id=original_slug, problem_update=problem_update)


def test_delete_problem_success(mock_db):
    # Mock existing problem
    unique_slug = f"test-problem-{uuid.uuid4()}"
    mock_problem = Problem(
        id=1,
        slug_id=unique_slug,
        title="Problem to Delete"
    )
    
    # Setup mock behavior
    mock_db.query.return_value.filter.return_value.first.return_value = mock_problem
    
    # Delete problem
    result = problems.delete_problem(db=mock_db, problem_id=unique_slug)
    
    # Check that delete was called
    assert result == mock_problem
    mock_db.delete.assert_called_once_with(mock_problem)
    mock_db.commit.assert_called_once()


def test_delete_problem_not_found(mock_db):
    # Mock behavior for non-existent problem
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Try to delete a non-existent problem
    with pytest.raises(ValueError, match="Problem with slug_id 'non-existent' not found."):
        problems.delete_problem(db=mock_db, problem_id="non-existent")


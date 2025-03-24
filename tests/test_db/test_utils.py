# tests/test_db/test_utils.py
from app.db.utils import get_db, init_db
import uuid
from app.db.models.category import Category
from app.db.models.problem import Problem
from unittest.mock import MagicMock

def test_get_db():
    db = next(get_db())
    assert db is not None
    db.close()

def test_init_db():
    init_db()
    # Assuming init_db prints "Creating tables..." and "Tables created successfully."
    # You can check the output or the existence of tables in the database.

def create_mock_category(name=None):
    """Create a mock category with a unique name if none provided"""
    if name is None:
        name = f"Test Category {uuid.uuid4()}"
    return Category(name=name, id=1)

def create_mock_problem(title=None, category=None):
    """Create a mock problem with optional title and category"""
    if title is None:
        title = f"Test Problem {uuid.uuid4()}"
    if category is None:
        category = create_mock_category()
        
    problem = Problem(
        title=title,
        slug_id=f"test-problem-{uuid.uuid4()}",
        difficulty="Medium",
        description="Test Description",
        examples=[
            {
                "input": "[1, 2, 3]",
                "output": "6",
                "explanation": "1 + 2 + 3 = 6"
            }
        ],
        id=1
    )
    problem.categories = [category]
    return problem

def setup_mock_db_query(mock_db_query, return_value):
    """Setup common mock query chain with a return value"""
    mock_query_chain = (
        mock_db_query.return_value
        .offset.return_value
        .limit.return_value
    )
    if isinstance(return_value, list):
        mock_query_chain.all.return_value = return_value
    else:
        mock_query_chain.first.return_value = return_value
    return mock_query_chain
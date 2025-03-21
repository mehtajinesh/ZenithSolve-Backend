# tests/test_crud/test_categories.py
from sqlalchemy.orm import Session
from app.crud import categories
from app.schemas.categories import Category
from app.db.models.category import Category
import uuid
from unittest.mock import MagicMock
import pytest


def test_create_category_existing(mock_db):
    # Mock existing category
    unique_name = f"Test Category {uuid.uuid4()}"
    mock_existing_category = Category(name=unique_name, id=1)
    
    # Setup mock behavior for existing category
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_category
    
    # Attempt to create a category that already exists
    category_in = Category(name=unique_name)
    
    with pytest.raises(Exception, match="Category already exists"):
        categories.create_category(db=mock_db, category=category_in)

def test_create_category_new(mock_db):
    # Create a unique category name
    unique_name = f"Test Category {uuid.uuid4()}"
    
    # Setup mock behavior for new category creation
    mock_db.query.return_value.filter.return_value.first.return_value = None  # No existing category
    
    # Create a new category
    category_in = Category(name=unique_name)
    
    # Mock the behavior of adding and committing to the database
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    created_category = categories.create_category(db=mock_db, category=category_in)
    
    # Check that the category was created correctly
    assert created_category.name == unique_name
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_get_categories(mock_db):
    # Mock existing categories
    mock_categories = [
        Category(name=f"Category {i}", id=i) for i in range(4)
    ]
    
    # Setup mock behavior for retrieving categories
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_categories
    
    # Call the function to get categories
    categories_list = categories.get_categories(db=mock_db, skip=0, limit=10)
    
    # Check that the retrieved categories match the mocked ones
    assert len(categories_list) == 4
    assert all(cat.startswith("Category") for cat in categories_list)
    assert all(isinstance(cat, str) for cat in categories_list)
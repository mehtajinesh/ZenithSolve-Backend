# tests/test_crud/test_categories.py
from app.crud import categories
from app.schemas.categories import Category
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

def test_update_category_existing(mock_db):
    # Mock existing category
    old_name = "Old Category"
    new_name = "New Category"
    mock_existing_category = Category(name=old_name, id=1)
    
    # Setup mock behavior for existing category
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_category
    
    # Create category schemas for update
    old_category = Category(name=old_name)
    new_category = Category(name=new_name)
    
    # Mock the behavior of committing and refreshing
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    
    # Update the category
    updated_category = categories.update_category(db=mock_db, old_category=old_category, new_category=new_category)
    
    # Check that the category was updated correctly
    assert updated_category.name == new_name
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_existing_category)

def test_update_category_not_found(mock_db):
    # Setup mock behavior for non-existent category
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Create category schemas for update
    old_category = Category(name="Non-existent Category")
    new_category = Category(name="New Name")
    
    # Attempt to update a non-existent category
    with pytest.raises(Exception, match=f"Category with name {old_category.name} not found."):
        categories.update_category(db=mock_db, old_category=old_category, new_category=new_category)

def test_delete_category_existing(mock_db):
    # Mock existing category
    category_name = "Category to Delete"
    mock_existing_category = Category(name=category_name, id=1)
    
    # Setup mock behavior for existing category
    mock_db.query.return_value.filter.return_value.first.return_value = mock_existing_category
    
    # Mock the behavior of deleting and committing
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()
    
    # Delete the category
    category_schema = Category(name=category_name)
    result = categories.delete_category(db=mock_db, category=category_schema)
    
    # Check that the deletion was successful
    assert result is True
    mock_db.delete.assert_called_once_with(mock_existing_category)
    mock_db.commit.assert_called_once()

def test_delete_category_not_found(mock_db):
    # Setup mock behavior for non-existent category
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Attempt to delete a non-existent category
    category_name = "Non-existent Category"
    category_schema = Category(name=category_name)
    
    with pytest.raises(Exception, match=f"Category with name {category_name} not found."):
        categories.delete_category(db=mock_db, category=category_schema)

# tests/test_crud/test_categories.py
from sqlalchemy.orm import Session
from app.crud import categories
from app.schemas.categories import CategoryCreate
from app.db.models.category import Category
import uuid

def test_create_category(db: Session):
    # Use a unique name to avoid conflicts
    unique_name = f"Test Category {uuid.uuid4()}"
    category_in = CategoryCreate(name=unique_name)
    category = categories.create_category(db=db, category=category_in)
    assert category.name == unique_name
    assert isinstance(category, Category)

def test_get_categories(db: Session):
    # Create unique categories
    unique_name1 = f"Test Category List1 {uuid.uuid4()}"
    unique_name2 = f"Test Category List2 {uuid.uuid4()}"
    category_in1 = CategoryCreate(name=unique_name1)
    category_in2 = CategoryCreate(name=unique_name2)
    
    cat1 = categories.create_category(db=db, category=category_in1)
    cat2 = categories.create_category(db=db, category=category_in2)
    
    # Get all categories
    fetched_categories = categories.get_categories(db=db, skip=0, limit=100)
    
    # Check that our created categories are in the list
    cat_ids = [c.id for c in fetched_categories]
    assert cat1.id in cat_ids
    assert cat2.id in cat_ids
# tests/test_crud/test_categories.py
from sqlalchemy.orm import Session
from app.crud import categories
from app.schemas.categories import CategoryCreate
from app.db.models.category import Category
from tests.conftest import db

def test_create_category(db: Session):
    category_in = CategoryCreate(name="Test Category")
    category = categories.create_category(db=db, category=category_in)
    assert category.name == "Test Category"
    assert isinstance(category, Category)

def test_get_category(db: Session):
    category_in = CategoryCreate(name="Test Category 2")
    category = categories.create_category(db=db, category=category_in)
    fetched_category = categories.get_category(db=db, category_id=category.id)
    assert fetched_category == category

def test_get_categories(db: Session):
    category_in1 = CategoryCreate(name="Test Category 3")
    category_in2 = CategoryCreate(name="Test Category 4")
    categories.create_category(db=db, category=category_in1)
    categories.create_category(db=db, category=category_in2)
    fetched_categories = categories.get_categories(db=db, skip=0, limit=10)
    assert len(fetched_categories) >= 2
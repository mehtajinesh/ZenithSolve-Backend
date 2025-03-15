from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.categories import Category, CategoryCreate
from app.db.utils import get_db
from app.crud import categories
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter()


@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        new_category = categories.create_category(db=db, category=category)
        return new_category
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category creation failed due to integrity constraints") from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred during category creation") from err
    except Exception as err:
        raise HTTPException(status_code=500, detail="An unexpected error occurred") from err

@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="skip and limit must be non-negative")
    try:
        retrieved_categories = categories.get_categories(db, skip=skip, limit=limit)
        return retrieved_categories
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error occurred while retrieving categories") from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred while retrieving categories") from err
    except Exception as err:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while retrieving categories") from err

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = categories.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

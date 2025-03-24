from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.categories import Category
from app.db.utils import get_db
from app.crud import categories
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.extras import format_response

router = APIRouter()

@format_response(Category)
@router.post("/categories/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: Category, db: Session = Depends(get_db)):
    """
    Creates a new category in the database.

    This function attempts to create a new category by interacting with the database
    through the categories.create_category function. It manages database transactions
    and handles various exceptions:

    - IntegrityError: Rolls back the transaction and raises an HTTP 400 error if there is an integrity constraint violation.
    - SQLAlchemyError: Rolls back the transaction and raises an HTTP 500 error if a database error occurs.
    - Exception: Raises an HTTP 500 error for any unexpected errors.

    Parameters:
        category (CategoryCreate): The data required to create a new category.
        db (Session, optional): The database session provided by Depends(get_db). Defaults to the session returned by get_db.

    Returns:
        The newly created category object if the operation is successful.

    Raises:
        HTTPException: 
            - 400: If an IntegrityError occurs due to integrity constraints.
            - 500: If a SQLAlchemyError or a generic Exception occurs.
    """
    try:
        new_category = categories.create_category(db=db, category=category)
        return new_category
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category with this name already exists") from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="A database error occurred during category creation") from err
    except Exception as err:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during category creation") from err
    


@format_response(List[str])
@router.get("/categories/", response_model=List[str])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of categories from the database using pagination.

    Parameters:
        skip (int): The number of categories to skip from the beginning of the query results. Must be non-negative.
        limit (int): The maximum number of categories to return. Must be non-negative.
        db (Session): The SQLAlchemy database session provided by FastAPI's dependency injection.

    Returns:
        The list of retrieved categories from the database.

    Raises:
        HTTPException: 
            - If 'skip' or 'limit' is negative (HTTP 400).
            - If a database integrity error occurs during the query (HTTP 400).
            - If a general SQLAlchemy error occurs during the query (HTTP 500).
            - For any other unexpected error (HTTP 500).
    """
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

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

    Parameters:
        category (CategoryCreate): The data required to create a new category.
        db (Session, optional): The database session provided by Depends(get_db).

    Returns:
        The newly created category object if the operation is successful.

    Raises:
        HTTPException: 
            - 400: If category already exists or other integrity constraints are violated
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        new_category = categories.create_category(db=db, category=category)
        return new_category
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Category with this name already exists",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred during category creation",
                "error": str(err)
            }
        ) from err
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred during category creation",
                "error": str(err)
            }
        ) from err

@format_response(List[str])
@router.get("/categories/", response_model=List[str])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieves a list of categories from the database using pagination.

    Parameters:
        skip (int): The number of categories to skip. Must be non-negative.
        limit (int): The maximum number of categories to return. Must be non-negative.
        db (Session): The database session.

    Returns:
        List[str]: The list of category names.

    Raises:
        HTTPException: 
            - 400: If pagination parameters are invalid
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    if skip < 0 or limit < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid pagination parameters",
                "error": "skip and limit must be non-negative"
            }
        )
    try:
        retrieved_categories = categories.get_categories(db, skip=skip, limit=limit)
        return retrieved_categories
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Database integrity error occurred",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while retrieving categories",
                "error": str(err)
            }
        ) from err
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while retrieving categories",
                "error": str(err)
            }
        ) from err

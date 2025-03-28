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
def read_categories(db: Session = Depends(get_db)):
    """
    Retrieves a list of categories from the database.

    Parameters:
        db (Session): The database session.

    Returns:
        List[str]: The list of category names.

    Raises:
        HTTPException: 
            - 400: If pagination parameters are invalid
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        retrieved_categories = categories.get_categories(db)
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

@format_response(Category)
@router.put("/categories/", response_model=Category)
def update_category(
    old_category: Category, new_category: Category, db: Session = Depends(get_db)
):
    """
    Updates an existing category in the database.

    This function updates a category name. It checks if the category exists and
    updates its fields with the provided data.

    Parameters:
        old_category (Category): The old name of the category to update.
        new_category (Category): The new data for the category.
        db (Session): The database session.

    Returns:
        Category: The updated category object.

    Raises:
        HTTPException: 
            - 404: If the category does not exist
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        updated_category = categories.update_category(db=db, old_category=old_category, new_category=new_category)
        return updated_category
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
                "message": "Database error occurred during category update",
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
                "message": "An unexpected error occurred during category update",
                "error": str(err)
            }
        ) from err

@format_response(bool)
@router.delete("/categories/", response_model=bool)
def delete_category(
    category: Category, db: Session = Depends(get_db)
):
    """
    Deletes a category from the database.

    This function deletes a category by its name. It checks if the category exists and
    deletes it from the database.

    Parameters:
        category (Category): The name of the category to delete.
        db (Session): The database session.

    Returns:
        bool: True if the deletion was successful, False otherwise.

    Raises:
        HTTPException: 
            - 404: If the category does not exist
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        deleted = categories.delete_category(db=db, category=category)
        return deleted
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
                "message": "Database error occurred during category deletion",
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
                "message": "An unexpected error occurred during category deletion",
                "error": str(err)
            }
        ) from err
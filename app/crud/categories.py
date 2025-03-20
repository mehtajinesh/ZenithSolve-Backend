from sqlalchemy.orm import Session
import app.db.models.category as models
import app.schemas.categories as schemas

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieves a list of categories from the database.

    This function queries the database for category records, applying pagination based on the provided
    skip and limit values.

    Parameters:
        db (Session): The SQLAlchemy session used for querying the database.
        skip (int, optional): The number of records to skip before returning results. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.

    Returns:
        List[models.Category]: A list of category objects retrieved from the database.
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Create a new category in the database, handling the case where the category already exists.

    This function takes in a database session and a category creation schema, checks if a category
    with the same name exists, and if not, creates a new Category model instance, adds it to the session,
    commits the transaction, and refreshes the instance with the latest data from the database.

    Args:
        db (Session): The SQLAlchemy session object used for database transactions.
        category (schemas.CategoryCreate): The data schema containing the necessary fields
            for creating a new category (e.g., name).

    Returns:
        models.Category: The newly created Category instance with updated fields (e.g., ID).

    Raises:
        Exception: If a category with the specified name already exists.
    """
    existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing_category:
        raise Exception("Category already exists")
    
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

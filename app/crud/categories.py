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
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    categories_names = [category.name for category in categories]
    return sorted(categories_names)

def create_category(db: Session, category: schemas.Category):
    """
    Create a new category in the database, handling the case where the category already exists.

    This function takes in a database session and a category creation schema, checks if a category
    with the same name exists, and if not, creates a new Category model instance, adds it to the session,
    commits the transaction, and refreshes the instance with the latest data from the database.

    Args:
        db (Session): The SQLAlchemy session object used for database transactions.
        category (schemas.Category): The data schema containing the necessary fields
            for creating a new category (e.g., name).

    Returns:
        models.Category: The newly created Category instance with updated fields (e.g., ID).

    Raises:
        Exception: If a category with the specified name already exists.
    """
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise Exception("Category already exists")
    # Create a new category
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, old_category: schemas.Category, new_category: schemas.Category):
    """
    Update an existing category in the database.

    This function takes in a database session, the old name of the category to be updated,
    and a new category name. It retrieves the existing category from the database,
    updates its fields with the new values, and commits the changes.

    Args:
        db (Session): The SQLAlchemy session object used for database transactions.
        old_category (schemas.Category): The old ename of the category to be updated.
        new_category (schemas.Category): The data schema containing the new values for the category.

    Returns:
        models.Category: The updated Category instance.

    Raises:
        Exception: If the specified category does not exist.
    """
    db_category = db.query(models.Category).filter(models.Category.name == old_category.name).first()
    if db_category is None:
        raise Exception(f"Category with name {old_category.name} not found.")
    
    db_category.name = new_category.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category: schemas.Category):
    """
    Delete a category from the database.

    This function takes in a database session and the ID of the category to be deleted.
    It retrieves the existing category from the database and deletes it.

    Args:
        db (Session): The SQLAlchemy session object used for database transactions.
        category (schemas.Category): The name of the category to be deleted.

    Returns:
        bool: True if the deletion was successful, False otherwise.

    Raises:
        Exception: If the specified category does not exist.
    """
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category is None:
        raise Exception(f"Category with name {category.name} not found.")
    
    db.delete(db_category)
    db.commit()
    return True
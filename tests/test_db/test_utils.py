# tests/test_db/test_utils.py
from app.db.utils import get_db, init_db

def test_get_db():
    db = next(get_db())
    assert db is not None
    db.close()

def test_init_db():
    init_db()
    # Assuming init_db prints "Creating tables..." and "Tables created successfully."
    # You can check the output or the existence of tables in the database.
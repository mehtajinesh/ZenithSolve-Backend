from app.db.database import SessionLocal, Base, engine
from app.db.models.category import Category
from app.db.models.problem import Problem
from app.db.models.real_world_example import RealWorldExample
from app.db.models.solution import Solution
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def init_db():
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
from db.database import SessionLocal, Base, engine
from db.models.category import Category
from db.models.problem import Problem
from db.models.real_world_example import RealWorldExample
from db.models.solution import Solution
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
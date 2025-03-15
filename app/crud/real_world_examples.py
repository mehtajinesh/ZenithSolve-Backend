from sqlalchemy.orm import Session
import app.db.models.real_world_example as models
import app.schemas.real_world_examples as schemas

def get_real_world_example(db: Session, example_id: int):
    return db.query(models.RealWorldExample).filter(models.RealWorldExample.id == example_id).first()

def get_real_world_examples(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.RealWorldExample).offset(skip).limit(limit).all()

def create_real_world_example(db: Session, example: schemas.RealWorldExampleCreate):
    db_example = models.RealWorldExample(
        description=example.description,
        business_impact=example.business_impact,
        consequences=example.consequences,
        problem_id=example.problem_id
    )
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example

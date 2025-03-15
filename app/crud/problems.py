from sqlalchemy.orm import Session
import app.db.models.problem as models
import app.schemas.problems as schemas

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()

def get_problems(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Problem).offset(skip).limit(limit).all()

def create_problem(db: Session, problem: schemas.ProblemCreate):
    db_problem = models.Problem(
        title=problem.title,
        statement=problem.statement,
        constraints=problem.constraints,
        examples=problem.examples,
        category_id=problem.category_id
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

from sqlalchemy.orm import Session
import db.models.solution as models
import schemas.solutions as schemas

def get_solution(db: Session, solution_id: int):
    return db.query(models.Solution).filter(models.Solution.id == solution_id).first()

def get_solutions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Solution).offset(skip).limit(limit).all()

def create_solution(db: Session, solution: schemas.SolutionCreate):
    db_solution = models.Solution(
        language=solution.language,
        code=solution.code,
        time_complexity=solution.time_complexity,
        space_complexity=solution.space_complexity,
        problem_id=solution.problem_id
    )
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution

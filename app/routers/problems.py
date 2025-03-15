from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.utils import get_db
from schemas.problems import Problem, ProblemCreate
from crud import problems
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter()

@router.post("/problems/", response_model=Problem)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    try:
        created_problem = problems.create_problem(db=db, problem=problem)
        return created_problem
    except IntegrityError as ie:
        # Likely a duplicate or bad data issue.
        raise HTTPException(status_code=400, detail="Integrity error: " + str(ie))
    except SQLAlchemyError as se:
        # Generic SQLAlchemy issues.
        raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
        # Catch-all for any other errors.
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/problems/", response_model=List[Problem])
def read_problems(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="Negative numbers are not allowed for skip or limit")
    try:
        retrieved_problems = problems.get_problems(db, skip=skip, limit=limit)
        return retrieved_problems
    except SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/problems/{problem_id}", response_model=Problem)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    db_problem = problems.get_problem(db, problem_id=problem_id)
    if db_problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem

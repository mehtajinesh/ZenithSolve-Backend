from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.utils import get_db
from app.schemas.solutions import SolutionCreate, Solution
from app.crud import solutions
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

router = APIRouter()

@router.post("/solutions/", response_model=Solution)
def create_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    try:
        created_solution = solutions.create_solution(db=db, solution=solution)
        return created_solution
    except IntegrityError as ie:
        # Likely a duplicate or bad data issue.
        raise HTTPException(status_code=400, detail="Integrity error: " + str(ie))
    except SQLAlchemyError as se:
        # Generic SQLAlchemy issues.
        raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
        # Catch-all for any other errors.
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/solutions/", response_model=List[Solution])
def read_solutions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="Negative numbers are not allowed for skip or limit")
    try:
        retrived_solutions = solutions.get_solutions(db, skip=skip, limit=limit)
        return retrived_solutions
    except SQLAlchemyError as se:
            raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
            raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/solutions/{solution_id}", response_model=Solution)
def read_solution(solution_id: int, db: Session = Depends(get_db)):
    db_solution = solutions.get_solution(db, solution_id=solution_id)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="Solution not found")
    return db_solution

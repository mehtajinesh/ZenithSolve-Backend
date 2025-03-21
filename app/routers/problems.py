from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.db.utils import get_db
from app.schemas.problems import ProblemIn, ProblemOut
from app.crud import problems
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.extras import format_response


router = APIRouter()

@format_response(ProblemOut)
@router.post("/problems/", response_model=ProblemOut)
def create_problem(problem: ProblemIn, db: Session = Depends(get_db)):
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

@format_response(ProblemOut)
@router.get("/problems/{problem_id}", response_model=ProblemOut)
def read_problem(problem_id: str, db: Session = Depends(get_db)):
    db_problem = problems.get_problem(db, slug_id=problem_id)
    return db_problem

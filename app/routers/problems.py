from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.db.utils import get_db
from app.schemas.problems import ProblemIn, ProblemOut
from app.schemas.solutions import Solution
from app.crud import problems
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.extras import format_response

router = APIRouter()

@format_response(ProblemOut)
@router.post("/problems/", response_model=ProblemOut, status_code=status.HTTP_201_CREATED)
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

@format_response(ProblemOut)
@router.get("/problems/{problem_id}", response_model=ProblemOut)
def read_problem(problem_id: str, db: Session = Depends(get_db)):
    db_problem = problems.get_problem(db, slug_id=problem_id)
    return db_problem

@format_response(List[ProblemOut])
@router.get("/problems/", response_model=List[ProblemOut])
def read_problems(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    """
    Retrieves a list of problems from the database using pagination.

    Parameters:
        skip (int): The number of problems to skip from the beginning of the query results. Must be non-negative.
        limit (int): The maximum number of problems to return. Must be positive.

    Returns:
        List[ProblemOut]: A list of problem objects.
    """
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    
    problems_list = problems.get_problems(db, skip=skip, limit=limit)
    return problems_list

# need a route to handle additing solutions to a problem
@format_response(Solution)
@router.post("/problems/{problem_id}/solutions", response_model=Solution,status_code=status.HTTP_201_CREATED)
def add_solution(problem_id: str, solution: Solution, db: Session = Depends(get_db)):
    """
    Adds a solution to a specific problem.

    Parameters:
        problem_id (str): The ID of the problem to which the solution will be added.
        solution (Solution): The solution data to be added.
        db (Session): The database session provided by Depends(get_db).

    Returns:
        SolutionOut: The newly created solution object.

    Raises:
        HTTPException: If the problem does not exist or if there is a database error.
    """
    try:        
        # Add the solution to the problem
        created_solution = problems.add_solution_to_problem(db=db, problem_id=problem_id, solution=solution)
        return created_solution
    except SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error: " + str(se))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
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
    """
    Creates a new problem in the database.

    Parameters:
        problem (ProblemIn): The problem data to create
        db (Session): The database session

    Returns:
        ProblemOut: The created problem

    Raises:
        HTTPException: 
            - 400: If problem already exists or other integrity constraints are violated
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        created_problem = problems.create_problem(db=db, problem=problem)
        return created_problem
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Database integrity error occurred",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred during problem creation",
                "error": str(err)
            }
        ) from err
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred during problem creation",
                "error": str(err)
            }
        ) from err

@format_response(ProblemOut)
@router.get("/problems/{problem_id}", response_model=ProblemOut)
def read_problem(problem_id: str, db: Session = Depends(get_db)):
    """
    Retrieves a specific problem by its ID.

    Parameters:
        problem_id (str): The ID of the problem to retrieve
        db (Session): The database session

    Returns:
        ProblemOut: The requested problem

    Raises:
        HTTPException: 
            - 404: If the problem is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        db_problem = problems.get_problem(db, slug_id=problem_id)
        if not db_problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Problem not found",
                    "error": f"No problem found with id {problem_id}"
                }
            )
        return db_problem
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid problem ID format",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while retrieving the problem",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while retrieving the problem",
                "error": str(err)
            }
        ) from err

@format_response(List[ProblemOut])
@router.get("/problems/", response_model=List[ProblemOut])
def read_problems(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    """
    Retrieves a list of problems using pagination.

    Parameters:
        skip (int): Number of problems to skip. Must be non-negative.
        limit (int): Maximum number of problems to return. Must be positive.
        db (Session): The database session

    Returns:
        List[ProblemOut]: List of problems

    Raises:
        HTTPException: 
            - 400: If pagination parameters are invalid
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid pagination parameters",
                "error": "skip must be non-negative and limit must be positive"
            }
        )
    try:
        problems_list = problems.get_problems(db, skip=skip, limit=limit)
        return problems_list
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while retrieving problems",
                "error": str(err)
            }
        ) from err
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while retrieving problems",
                "error": str(err)
            }
        ) from err

@format_response(Solution)
@router.post("/problems/{problem_id}/solutions", response_model=Solution, status_code=status.HTTP_201_CREATED)
def add_solution(problem_id: str, solution: Solution, db: Session = Depends(get_db)):
    """
    Adds a solution to a specific problem.

    Parameters:
        problem_id (str): The ID of the problem
        solution (Solution): The solution data to add
        db (Session): The database session

    Returns:
        Solution: The created solution

    Raises:
        HTTPException: 
            - 404: If the problem is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        created_solution = problems.add_solution_to_problem(db=db, problem_id=problem_id, solution=solution)
        return created_solution
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Problem not found",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while adding solution",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while adding solution",
                "error": str(err)
            }
        ) from err

@format_response(ProblemOut)
@router.put("/problems/{problem_id}", response_model=ProblemOut)
def update_problem(problem_id: str, problem: ProblemIn, db: Session = Depends(get_db)):
    """
    Updates a specific problem by its ID.

    Parameters:
        problem_id (str): The ID of the problem to update
        problem (ProblemIn): The updated problem data
        db (Session): The database session

    Returns:
        ProblemOut: The updated problem

    Raises:
        HTTPException: 
            - 404: If the problem is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        updated_problem = problems.update_problem(db=db, problem_id=problem_id, problem_update=problem)
        if not updated_problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Problem not found",
                    "error": f"No problem found with id {problem_id}"
                }
            )
        return updated_problem
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while updating the problem",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while updating the problem",
                "error": str(err)
            }
        ) from err

@router.delete("/problems/{problem_id}")
def delete_problem(problem_id: str, db: Session = Depends(get_db)):
    """
    Deletes a specific problem by its ID.

    Parameters:
        problem_id (str): The ID of the problem to delete
        db (Session): The database session

    Returns:
        bool: True if the problem was deleted successfully
    Raises:
        HTTPException: 
            - 404: If the problem is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        deleted_problem = problems.delete_problem(db=db, problem_id=problem_id)
        if not deleted_problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Problem not found",
                    "error": f"No problem found with id {problem_id}"
                }
            )
        return True
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while deleting the problem",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while deleting the problem",
                "error": str(err)
            }
        ) from err

@router.delete("/problems/{problem_id}/solutions/{solution_name}")
def delete_solution(problem_id: str, solution_name: str, db: Session = Depends(get_db)):
    """
    Deletes a specific solution from a problem.

    Parameters:
        problem_id (str): The ID of the problem
        solution_name (str): The name of the solution to delete
        db (Session): The database session

    Returns:
        bool: True if the solution was deleted successfully 

    Raises:
        HTTPException: 
            - 404: If the problem or solution is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        deleted_solution = problems.delete_solution(db=db, problem_id=problem_id, solution_name=solution_name)
        if not deleted_solution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Solution not found",
                    "error": f"No solution found with name {solution_name} for problem {problem_id}"
                }
            )
        return True
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while deleting the solution",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while deleting the solution",
                "error": str(err)
            }
        ) from err

@format_response(Solution)
@router.put("/problems/{problem_id}/solutions/{solution_name}", response_model=Solution)
def update_solution(problem_id: str, solution_name: str, solution: Solution, db: Session = Depends(get_db)):
    """
    Updates a specific solution for a problem.

    Parameters:
        problem_id (str): The ID of the problem
        solution_name (str): The name of the solution to update
        solution (Solution): The updated solution data
        db (Session): The database session

    Returns:
        Solution: The updated solution

    Raises:
        HTTPException: 
            - 404: If the problem or solution is not found
            - 422: If validation fails
            - 500: If a database or unexpected error occurs
    """
    try:
        updated_solution = problems.update_solution(db=db, problem_id=problem_id, solution_name=solution_name, solution_update=solution)
        if not updated_solution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Solution not found",
                    "error": f"No solution found with name {solution_name} for problem {problem_id}"
                }
            )
        return updated_solution
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "Invalid data provided",
                "error": str(err)
            }
        ) from err
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Database error occurred while updating the solution",
                "error": str(err)
            }
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "An unexpected error occurred while updating the solution",
                "error": str(err)
            }
        ) from err
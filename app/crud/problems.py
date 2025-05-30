from sqlalchemy.orm import Session
import json
from app.db.models.problem import Problem
from app.db.models.solution import Solution
from app.db.models.category import Category
import app.schemas.problems as schemas
from app.extras import compare_approaches

def get_problems(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieves a list of problems from the database using pagination.

    Parameters:
        db (Session): The database session.
        skip (int): The number of problems to skip from the beginning of the query results. Must be non-negative.
        limit (int): The maximum number of problems to return. Must be positive.

    Returns:
        List[schemas.ProblemOut]: A list of problem objects.
    """
    if skip < 0 or limit <= 0:
        raise ValueError("Invalid pagination parameters")
    
    problems = db.query(Problem).offset(skip).limit(limit).all()
    return [schemas.ProblemOut(
        slug_id=problem.slug_id,
        title=problem.title,
        difficulty=problem.difficulty,
        description=problem.description,
        constraints=problem.constraints,
        examples= problem.examples,
        categories=[cat.name for cat in problem.categories] if problem.categories else [],
        best_time_complexity=problem.best_time_complexity,
        best_space_complexity=problem.best_space_complexity,
        solutions=[schemas.Solution(**solution.__dict__) for solution in problem.solutions] if problem.solutions else [],
        real_world_applications=[schemas.RealWorldExample(**example.__dict__) for example in problem.real_world_examples] if problem.real_world_examples else []
    ) for problem in problems]

def get_problem(db: Session, slug_id: str):
    # check if problem with the given slug_id exists
    problem = db.query(Problem).filter(Problem.slug_id == slug_id).first() 
    if not problem:
        raise ValueError(f"Problem with slug_id '{slug_id}' not found.")
    problem_out = {
        "slug_id": problem.slug_id,
        "title": problem.title,
        "difficulty": problem.difficulty,
        "description": problem.description,
        "constraints": problem.constraints,
        "examples": problem.examples,
        "clarifying_questions": problem.clarifying_questions,
        "categories": [cat.name for cat in problem.categories] if problem.categories else [],
        "best_time_complexity": problem.best_time_complexity,
        "best_space_complexity": problem.best_space_complexity,
        "solutions": [schemas.Solution(**solution.__dict__) for solution in problem.solutions] if problem.solutions else [],
        "real_world_applications": [schemas.RealWorldExample(**example.__dict__) for example in problem.real_world_examples] if problem.real_world_examples else []
    }
    return schemas.ProblemOut(**problem_out)

def create_problem(db: Session, problem: schemas.ProblemIn):
    
    # Check for existing problem with the same slug_id
    existing_problem = db.query(Problem).filter(Problem.slug_id == problem.slug_id).first() 
    if existing_problem:
        raise ValueError(f"Problem with slug_id '{problem.slug_id}' already exists.")

    # check if categories exist
    if problem.categories:
        categories = db.query(Category).filter(Category.name.in_(problem.categories)).all()
        if len(categories) != len(problem.categories):
            raise ValueError("One or more categories do not exist.")
    
    # Create new problem with data from schema
    db_problem = Problem(
        slug_id=problem.slug_id,
        title=problem.title,
        difficulty=problem.difficulty,
        categories=categories,
        description=problem.description,
        constraints=problem.constraints,
        examples=problem.examples,
        clarifying_questions=problem.clarifying_questions
    )
    
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)

    problem_out = {
        "slug_id": db_problem.slug_id,
        "title": db_problem.title,
        "difficulty": db_problem.difficulty,
        "description": db_problem.description,
        "constraints": db_problem.constraints,
        "examples": problem.examples,
        "clarifying_questions": problem.clarifying_questions,
        "categories": problem.categories,
        "best_time_complexity": "NA",
        "best_space_complexity": "NA",
        "solutions": [],
        "real_world_applications": []
    }
    return schemas.ProblemOut(**problem_out)

def add_solution_to_problem(db: Session, problem_id: int, solution: schemas.Solution):
    problem = db.query(Problem).filter(Problem.slug_id == problem_id).first() 
    if not problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
    # Check if the solution already exists
    existing_solution = db.query(Solution).filter(Solution.name == solution.name, Solution.problem_id == problem.id).first()
    if existing_solution:
        raise ValueError(f"Solution with name '{solution.name}' already exists for problem '{problem_id}'.")
    # Add the solution to the db and link it to the problem
    solution = Solution( name=solution.name,
                        code=solution.code,
                        description=solution.description,
                        time_complexity=solution.time_complexity,
                        space_complexity=solution.space_complexity,
                        problem_id=problem.id)
    db.add(solution)
    db.commit()
    db.refresh(solution)

    # Update the problem's best time and space complexity if the new solution is better
    problem.best_time_complexity, problem.best_space_complexity = compare_approaches(solution.time_complexity, solution.space_complexity, problem.best_time_complexity, problem.best_space_complexity)
    db.commit()
    solution_op = {
        "name": solution.name,
        "code": solution.code,
        "description": solution.description,
        "time_complexity": solution.time_complexity,
        "space_complexity": solution.space_complexity,
    }
    return schemas.Solution(**solution_op)

def update_problem(db: Session, problem_id: int, problem_update: schemas.ProblemIn):
    db_problem = db.query(Problem).filter(Problem.slug_id == problem_id).first()
    # Check if the problem exists
    if not db_problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
    # Check if categories exist
    if problem_update.categories:
        categories = db.query(Category).filter(Category.name.in_(problem_update.categories)).all()
        if len(categories) != len(problem_update.categories):
            raise ValueError("One or more categories do not exist.")
    
    # Update scalar attributes
    for key, value in problem_update.__dict__.items():
        if key in ["slug_id", "examples", "categories", "clarifying_questions"]:
            continue
        setattr(db_problem, key, value)
    
    # Update the slug_id if it has changed
    if problem_update.slug_id != db_problem.slug_id:
        existing_problem = db.query(Problem).filter(Problem.slug_id == problem_update.slug_id).first()
        if existing_problem:
            raise ValueError(f"Problem with slug_id '{problem_update.slug_id}' already exists.")
    
    db_problem.slug_id = problem_update.slug_id
    db_problem.examples = problem_update.examples
    db_problem.clarifying_questions = problem_update.clarifying_questions
    db_problem.categories = categories
    
    db.commit()
    db.refresh(db_problem)

    problem_op = {
        "slug_id": db_problem.slug_id,
        "title": db_problem.title,
        "difficulty": db_problem.difficulty,
        "description": db_problem.description,
        "constraints": db_problem.constraints,
        "examples": db_problem.examples,
        "clarifying_questions": db_problem.clarifying_questions,
        "categories": [cat.name for cat in db_problem.categories] if db_problem.categories else [],
        "best_time_complexity": db_problem.best_time_complexity,
        "best_space_complexity": db_problem.best_space_complexity,
        "solutions": [schemas.Solution(**solution.__dict__) for solution in db_problem.solutions] if db_problem.solutions else [],
        "real_world_applications": [schemas.RealWorldExample(**example.__dict__) for example in db_problem.real_world_examples] if db_problem.real_world_examples else []
    }
    return problem_op

def delete_problem(db: Session, problem_id: int):
    db_problem = db.query(Problem).filter(Problem.slug_id == problem_id).first()
    if not db_problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
    db.delete(db_problem)
    db.commit()
    return db_problem

def update_solution(db: Session, solution_name: str, problem_id: int, solution_update: schemas.Solution):
    # Check if the problem exists
    db_problem = db.query(Problem).filter(Problem.slug_id == problem_id).first()
    if not db_problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
    # Check if the solution exists
    db_solution = db.query(Solution).filter(Solution.name == solution_name, Solution.problem_id == db_problem.id).first()
    if not db_solution:
        raise ValueError(f"Solution with name '{solution_name}' not found in problem '{problem_id}'.")
    # Update scalar attributes
    for key, value in solution_update.__dict__.items():
        setattr(db_solution, key, value)
    
    # Update the solution in the database
    db.commit()
    db.refresh(db_solution)
    return db_solution

def delete_solution(db: Session, solution_name: str, problem_id: int):
    # Check if the problem exists
    db_problem = db.query(Problem).filter(Problem.slug_id == problem_id).first()
    if not db_problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
    # Check if the solution exists
    db_solution = db.query(Solution).filter(Solution.name == solution_name, Solution.problem_id == db_problem.id).first()
    if not db_solution:
        raise ValueError(f"Solution with name '{solution_name}' not found in problem '{problem_id}'.")
    # Delete the solution
    db.delete(db_solution)
    db.commit()
    return db_solution
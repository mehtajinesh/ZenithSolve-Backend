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
        examples= [schemas.ExampleItem(**example) for example in json.loads(problem.examples)] if problem.examples else [],
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
        "examples": [schemas.ExampleItem(**example) for example in json.loads(problem.examples)] if problem.examples else [],
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
    
    # check if examples are provided or not, if yes, check if schema is valid
    if problem.examples:
        for example in problem.examples:
            if not isinstance(example, schemas.ExampleItem):
                raise ValueError("Invalid example schema provided.")
    
    json_examples = json.dumps([example.__dict__ for example in problem.examples])
    # Create new problem with data from schema
    db_problem = Problem(
        slug_id=problem.slug_id,
        title=problem.title,
        difficulty=problem.difficulty,
        categories=categories,
        description=problem.description,
        constraints=problem.constraints,
        examples=json_examples
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
        "categories": problem.categories,
        "best_time_complexity": "NA",
        "best_space_complexity": "NA",
        "solutions": [],
        "real_world_applications": []
    }
    return schemas.ProblemOut(**problem_out)

def update_problem(db: Session, problem_id: int, problem_update: schemas.ProblemIn):
    db_problem = get_problem(db, problem_id=problem_id)
    if not db_problem:
        return None
    
    # Update scalar attributes
    for key, value in problem_update.dict(exclude={'category_ids', 'examples'}).items():
        setattr(db_problem, key, value)
    
    # Convert examples list to JSON string for storage
    if problem_update.examples:
        db_problem.examples = json.dumps([example.dict() for example in problem_update.examples])
    
    # Update categories if provided
    if problem_update.categories:
        categories = db.query(Category).filter(Category.id.in_(problem_update.categories)).all()
        db_problem.categories = categories
    
    db.commit()
    db.refresh(db_problem)
    return db_problem

def add_solution_to_problem(db: Session, problem_id: int, solution: schemas.Solution):
    problem = db.query(Problem).filter(Problem.slug_id == problem_id).first() 
    if not problem:
        raise ValueError(f"Problem with slug_id '{problem_id}' not found.")
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
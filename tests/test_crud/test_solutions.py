# tests/test_crud/test_solutions.py
from sqlalchemy.orm import Session
from app.crud import solutions, categories, problems
from app.schemas.solutions import SolutionCreate
from app.schemas.categories import CategoryCreate
from app.schemas.problems import ProblemCreate
from app.db.models.solution import Solution
from tests.conftest import db

def test_create_solution(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem = problems.get_problem(db=db, problem_id=1)
    if not problem:
        problem_in = ProblemCreate(
            title="Test Problem",
            statement="Test Statement",
            constraints="Test Constraints",
            examples="Test Examples",
            category_id=category.id
        )
        problem = problems.create_problem(db=db, problem=problem_in)
    solution_in = SolutionCreate(
        language="Python",
        code="print('Hello, World!')",
        time_complexity="O(1)",
        space_complexity="O(1)",
        problem_id=problem.id
    )
    solution = solutions.create_solution(db=db, solution=solution_in)
    assert solution.language == "Python"
    assert isinstance(solution, Solution)

def test_get_solution(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem = problems.get_problem(db=db, problem_id=1)
    if not problem:
        problem_in = ProblemCreate(
            title="Test Problem",
            statement="Test Statement",
            constraints="Test Constraints",
            examples="Test Examples",
            category_id=category.id
        )
        problem = problems.create_problem(db=db, problem=problem_in)
    solution_in = SolutionCreate(
        language="Python",
        code="print('Hello, World!')",
        time_complexity="O(1)",
        space_complexity="O(1)",
        problem_id=problem.id
    )
    solution = solutions.create_solution(db=db, solution=solution_in)
    fetched_solution = solutions.get_solution(db=db, solution_id=solution.id)
    assert fetched_solution == solution

def test_get_solutions(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem = problems.get_problem(db=db, problem_id=1)
    if not problem:
        problem_in = ProblemCreate(
            title="Test Problem",
            statement="Test Statement",
            constraints="Test Constraints",
            examples="Test Examples",
            category_id=category.id
        )
        problem = problems.create_problem(db=db, problem=problem_in)
    solution_in1 = SolutionCreate(
        language="Python",
        code="print('Hello, World!')",
        time_complexity="O(1)",
        space_complexity="O(1)",
        problem_id=problem.id
    )
    solution_in2 = SolutionCreate(
        language="JavaScript",
        code="console.log('Hello, World!')",
        time_complexity="O(1)",
        space_complexity="O(1)",
        problem_id=problem.id
    )
    solutions.create_solution(db=db, solution=solution_in1)
    solutions.create_solution(db=db, solution=solution_in2)
    fetched_solutions = solutions.get_solutions(db=db, skip=0, limit=10)
    assert len(fetched_solutions) >= 2
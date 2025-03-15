# tests/test_crud/test_problems.py
from sqlalchemy.orm import Session
from app.crud import problems, categories
from app.schemas.problems import ProblemCreate
from app.schemas.categories import CategoryCreate
from app.db.models.problem import Problem
from tests.conftest import db


def test_create_problem(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem_in = ProblemCreate(
        title="Test Problem",
        statement="Test Statement",
        constraints="Test Constraints",
        examples="Test Examples",
        category_id=category.id
    )
    problem = problems.create_problem(db=db, problem=problem_in)
    assert problem.title == "Test Problem"
    assert isinstance(problem, Problem)

def test_get_problem(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem_in = ProblemCreate(
        title="Test Problem",
        statement="Test Statement",
        constraints="Test Constraints",
        examples="Test Examples",
        category_id=category.id
    )
    problem = problems.create_problem(db=db, problem=problem_in)
    fetched_problem = problems.get_problem(db=db, problem_id=problem.id)
    assert fetched_problem == problem

def test_get_problems(db: Session):
    category = categories.get_category(db=db, category_id=1)
    if not category:
        category_in = CategoryCreate(name="Test Category")
        category = categories.create_category(db=db, category=category_in)
    problem_in1 = ProblemCreate(
        title="Test Problem 1",
        statement="Test Statement 1",
        constraints="Test Constraints 1",
        examples="Test Examples 1",
        category_id=category.id
    )
    problem_in2 = ProblemCreate(
        title="Test Problem 2",
        statement="Test Statement 2",
        constraints="Test Constraints 2",
        examples="Test Examples 2",
        category_id=category.id
    )
    problems.create_problem(db=db, problem=problem_in1)
    problems.create_problem(db=db, problem=problem_in2)
    fetched_problems = problems.get_problems(db=db, skip=0, limit=10)
    assert len(fetched_problems) >= 2
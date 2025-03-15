# tests/test_crud/test_real_world_examples.py
from sqlalchemy.orm import Session
from app.crud import real_world_examples, categories, problems
from app.schemas.real_world_examples import RealWorldExampleCreate
from app.schemas.categories import CategoryCreate
from app.schemas.problems import ProblemCreate
from app.db.models.real_world_example import RealWorldExample
from tests.conftest import db

def test_create_real_world_example(db: Session):
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
    example_in = RealWorldExampleCreate(
        description="Test Description",
        business_impact="Test Impact",
        consequences="Test Consequences",
        problem_id=problem.id
    )
    example = real_world_examples.create_real_world_example(db=db, example=example_in)
    assert example.description == "Test Description"
    assert isinstance(example, RealWorldExample)

def test_get_real_world_example(db: Session):
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
    example_in = RealWorldExampleCreate(
        description="Test Description",
        business_impact="Test Impact",
        consequences="Test Consequences",
        problem_id=problem.id
    )
    example = real_world_examples.create_real_world_example(db=db, example=example_in)
    fetched_example = real_world_examples.get_real_world_example(db=db, example_id=example.id)
    assert fetched_example == example

def test_get_real_world_examples(db: Session):
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
    example_in1 = RealWorldExampleCreate(
        description="Test Description 1",
        business_impact="Test Impact 1",
        consequences="Test Consequences 1",
        problem_id=problem.id
    )
    example_in2 = RealWorldExampleCreate(
        description="Test Description 2",
        business_impact="Test Impact 2",
        consequences="Test Consequences 2",
        problem_id=problem.id
    )
    real_world_examples.create_real_world_example(db=db, example=example_in1)
    real_world_examples.create_real_world_example(db=db, example=example_in2)
    fetched_examples = real_world_examples.get_real_world_examples(db=db, skip=0, limit=10)
    assert len(fetched_examples) >= 2
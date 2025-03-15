from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.utils import get_db
from schemas.real_world_examples import RealWorldExample, RealWorldExampleCreate
from crud import real_world_examples 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


router = APIRouter()

@router.post("/real_world_examples/", response_model=RealWorldExample)
def create_real_world_example(example: RealWorldExampleCreate, db: Session = Depends(get_db)):
    try:
        created_real_world_example = real_world_examples.create_real_world_example(db=db, example=example)
        return created_real_world_example
    except IntegrityError as ie:
        # Likely a duplicate or bad data issue.
        raise HTTPException(status_code=400, detail="Integrity error: " + str(ie))
    except SQLAlchemyError as se:
        # Generic SQLAlchemy issues.
        raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
        # Catch-all for any other errors.
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/real_world_examples/", response_model=List[RealWorldExample])
def read_real_world_examples(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="Negative numbers are not allowed for skip or limit")
    try:
        examples = real_world_examples.get_real_world_examples(db, skip=skip, limit=limit)
        return examples
    except SQLAlchemyError as se:
        raise HTTPException(status_code=500, detail="Database error: " + str(se))
    except Exception as ex:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(ex))

@router.get("/real_world_examples/{example_id}", response_model=RealWorldExample)
def read_real_world_example(example_id: int, db: Session = Depends(get_db)):
    db_example = real_world_examples.get_real_world_example(db, example_id=example_id)
    if db_example is None:
        raise HTTPException(status_code=404, detail="RealWorldExample not found")
    return db_example

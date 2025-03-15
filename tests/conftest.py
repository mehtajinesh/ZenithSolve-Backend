# tests/conftest.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.models.category import Category
from app.db.models.problem import Problem
from app.db.models.solution import Solution
from app.db.models.real_world_example import RealWorldExample
import pytest
from dotenv import load_dotenv
from omegaconf import OmegaConf
import os
load_dotenv()

config = OmegaConf.load(f"config/db.yaml")

SQLALCHEMY_DATABASE_URL = f'postgresql://{config.db.username}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

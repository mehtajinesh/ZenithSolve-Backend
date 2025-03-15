from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from omegaconf import OmegaConf
from dotenv import load_dotenv

load_dotenv()

config = OmegaConf.load('config/db.yaml')


SQLALCHEMY_DATABASE_URL = f'postgresql://{config.db.username}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




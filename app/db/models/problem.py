from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table, ARRAY
from sqlalchemy.orm import relationship
from app.db.database import Base

# Many-to-many relationship table for problems and categories
problem_category = Table(
    'problem_category',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True, index=True)
    slug_id = Column(String, unique=True, index=True)  # For URL-friendly ID like 'two-sum'
    title = Column(String, index=True)
    difficulty = Column(String)
    categories = relationship('Category', secondary=problem_category, back_populates='problems')
    description = Column(Text)
    constraints = Column(ARRAY(String), default=[])
    examples = Column(Text)
    best_time_complexity = Column(String, default="NA")
    best_space_complexity = Column(String, default="NA")
    real_world_examples = relationship('RealWorldExample', back_populates='problem')
    solutions = relationship('Solution', back_populates='problem')

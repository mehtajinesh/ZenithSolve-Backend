from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    statement = Column(Text)
    constraints = Column(Text)
    examples = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='problems')
    real_world_examples = relationship('RealWorldExample', back_populates='problem')
    solutions = relationship('Solution', back_populates='problem')

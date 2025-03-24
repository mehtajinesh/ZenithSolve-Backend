from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class RealWorldExample(Base):
    __tablename__ = 'real_world_examples'

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String)  # Industry (e.g., "E-commerce", "Finance")
    description = Column(Text)  # Description of the application
    impact = Column(String)  # Business impact (e.g., "Improves checkout optimization by 27%")
    problem_id = Column(Integer, ForeignKey('problems.id'))
    problem = relationship('Problem', back_populates='real_world_examples')

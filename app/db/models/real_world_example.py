from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class RealWorldExample(Base):
    __tablename__ = 'real_world_examples'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    business_impact = Column(String)
    consequences = Column(String)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    problem = relationship('Problem', back_populates='real_world_examples')

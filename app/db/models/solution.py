from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Solution(Base):
    __tablename__ = 'solutions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # Name of the approach (e.g., "Hash Table Approach")
    description = Column(Text)  # Description of the approach
    code = Column(Text)
    time_complexity = Column(String)
    space_complexity = Column(String)
    problem_id = Column(Integer, ForeignKey('problems.id'))
    problem = relationship('Problem', back_populates='solutions')
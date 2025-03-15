from pydantic import BaseModel

class SolutionBase(BaseModel):
    language: str
    code: str
    time_complexity: str
    space_complexity: str
    problem_id: int

class SolutionCreate(SolutionBase):
    pass

class Solution(SolutionBase):
    id: int

    class Config:
        orm_mode = True

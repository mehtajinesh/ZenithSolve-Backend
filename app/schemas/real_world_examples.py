from pydantic import BaseModel

class RealWorldExampleBase(BaseModel):
    description: str
    business_impact: str
    consequences: str
    problem_id: int

class RealWorldExampleCreate(RealWorldExampleBase):
    pass

class RealWorldExample(RealWorldExampleBase):
    id: int

    class Config:
        orm_mode = True

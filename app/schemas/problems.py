from pydantic import BaseModel
from typing import List
from app.schemas.real_world_examples import RealWorldExample
from app.schemas.solutions import Solution
from pydantic import Field
from enum import Enum

class ExampleItem(BaseModel):
    input: str
    output: str
    explanation: str

class ProblemDifficultyEnum(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ProblemIn(BaseModel):
    slug_id: str = Field(..., description="Unique identifier for the problem")
    title: str = Field(..., description="Title of the problem")
    difficulty: ProblemDifficultyEnum = Field(..., description="Difficulty of the problem [Easy, Medium, Hard]")
    categories: List[str] = Field(default=[], description="List of categories associated with the problem")
    description: str = Field(..., description="Detailed description of the problem")
    constraints: List[str] = Field(default=[], description="List of constraints for the problem")
    examples: List[ExampleItem] = Field(..., description="List of example inputs and outputs for the problem")

    class Config:
        use_enum_values = True
        from_attributes = True
    
    @property
    def categories(self):
        return [cat.name for cat in self.categories] if self.categories else []
    
    @property
    def examples(self):
        return [example.__dict__ for example in self.examples] if self.examples else []

class ProblemOut(ProblemIn):
    solution_approach: str = Field(description="Approach to solve the problem")
    best_time_complexity: str = Field(description="Best time complexity of the solution")
    best_space_complexity: str = Field(description="Best space complexity of the solution")
    solutions: List[Solution] = Field(default=[], description="List of solutions for the problem")
    real_world_applications: List[RealWorldExample] = Field(default=[], description="List of real-world applications of the problem")
    
    class Config:
        from_attributes = True
        
    # Alias properties to match the frontend expected JSON
    @property
    def real_world_applications(self):
        return self.real_world_examples
        
    @property
    def pythonSolutions(self):
        return [s for s in self.solutions if s.language == "Python"]

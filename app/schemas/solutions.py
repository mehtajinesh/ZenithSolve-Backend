from pydantic import BaseModel

class Solution(BaseModel):
    name: str
    description: str
    code: str
    time_complexity: str
    space_complexity: str

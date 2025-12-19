from pydantic import BaseModel
from typing import List, Optional

class RequirementInput(BaseModel):
    id: str
    title: str
    description: str
    acceptance_criteria: Optional[List[str]] = []
    nfrs: Optional[List[str]] = []

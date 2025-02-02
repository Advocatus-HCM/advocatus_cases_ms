from pydantic import BaseModel
from typing import List
from datetime import datetime

class Personnel(BaseModel):
    person_id: str
    name: str
    role: str

class Case(BaseModel):
    name: str
    description: str
    start_date: datetime
    type: str
    subtype: str
    status: str
    archived: bool = False
    involved_personnel: List[Personnel]
    created_at: datetime
    updates_at: datetime
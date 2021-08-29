from typing import Optional, List
from pydantic import BaseModel

class TodoCreate(BaseModel):
    description: str
    isDone: Optional[float] = False

class Todo(BaseModel):
    id: int
    description: str
    isDone: bool
    
    class Config:
        orm_mode = True

class Credit(BaseModel):
    name: str
    value: float
    status: str

class Debit(BaseModel):
    name: str
    value: float
    status: str

class BillingCycleCreate(BaseModel):
    name: str
    month: int
    year: int
    debits: List[Optional[Debit]]
    credits: List[Optional[Credit]]

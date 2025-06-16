from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class PlanBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    precio: float
    rol: str = Field(..., max_length=50)
    duracion: int  # días

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    rol: Optional[str] = None
    duracion: Optional[int] = None

class PlanRead(PlanBase):
    id: int
    class Config:
        orm_mode = True
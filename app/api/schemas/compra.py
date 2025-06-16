from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class CompraBase(BaseModel):
    id_usuario: int
    id_plan: int
    url_pago: str
    id_transaccion: str
    estado_pago: str
    activo: bool = False
    fecha_compra: datetime
    fecha_finalizacion: datetime

class CompraCreate(CompraBase):
    pass

class CompraUpdate(BaseModel):
    estado_pago: Optional[str] = None
    activo: Optional[bool] = None

class CompraRead(CompraBase):
    id: int
    class Config:
        orm_mode = True
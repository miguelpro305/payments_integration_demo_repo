from api.schemas.compra import CompraCreate, CompraRead, CompraUpdate
from api.services.compra import CompraService
from database.db import get_db
from database.repositories import CompraRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/compras", tags=["compras"])

# Dependencia para inyectar el servicio

def get_compra_service(session: Session = Depends(get_db)) -> CompraService:
    repo = CompraRepository(session)
    return CompraService(repo)

@router.post("/", response_model=CompraRead)
async def create_compra(data: CompraCreate, svc: CompraService = Depends(get_compra_service)):
    return await svc.create_compra(data)


@router.get("/{compra_id}", response_model=CompraRead)
async def read_compra(compra_id: int, svc: CompraService = Depends(get_compra_service)):
    obj = svc.get_compra(compra_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Compra not found")
    return obj

@router.get("/", response_model=list[CompraRead])
async def list_compras(skip: int = 0, limit: int = 100, svc: CompraService = Depends(get_compra_service)):
    return svc.list_compras(skip, limit)

@router.put("/{compra_id}", response_model=CompraRead)
async def update_compra(compra_id: int, data: CompraUpdate, svc: CompraService = Depends(get_compra_service)):
    obj = svc.update_compra(compra_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Compra not found")
    return obj

@router.delete("/{compra_id}")
async def delete_compra(compra_id: int, svc: CompraService = Depends(get_compra_service)):
    success = svc.delete_compra(compra_id)
    if not success:
        raise HTTPException(status_code=404, detail="Compra not found")
    return {"ok": True}
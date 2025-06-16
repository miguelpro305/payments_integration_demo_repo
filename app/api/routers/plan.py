from api.schemas.plan import PlanCreate, PlanRead, PlanUpdate
from api.services.plan import PlanService
from database.db import get_db
from database.repositories import PlanRepository
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/plans", tags=["plans"])

# Dependencia para inyectar el servicio

def get_plan_service(session: Session = Depends(get_db)) -> PlanService:
    repo = PlanRepository(session)
    return PlanService(repo)

@router.post("/", response_model=PlanRead)
async def create_plan(data: PlanCreate, svc: PlanService = Depends(get_plan_service)):
    return svc.create_plan(data)

@router.get("/{plan_id}", response_model=PlanRead)
async def read_plan(plan_id: int, svc: PlanService = Depends(get_plan_service)):
    obj = svc.get_plan(plan_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Plan not found")
    return obj

@router.get("/", response_model=list[PlanRead])
async def list_plans(skip: int = 0, limit: int = 100, svc: PlanService = Depends(get_plan_service)):
    return svc.list_plans(skip, limit)

@router.put("/{plan_id}", response_model=PlanRead)
async def update_plan(plan_id: int, data: PlanUpdate, svc: PlanService = Depends(get_plan_service)):
    obj = svc.update_plan(plan_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Plan not found")
    return obj

@router.delete("/{plan_id}")
async def delete_plan(plan_id: int, svc: PlanService = Depends(get_plan_service)):
    success = svc.delete_plan(plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"ok": True}
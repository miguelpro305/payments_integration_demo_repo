from typing import Optional
from api.schemas.compra import CompraCreate, CompraUpdate
from api.schemas.plan import PlanCreate, PlanUpdate
from database.models import Compra, Plan
from sqlalchemy.orm import Session


class PlanRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, plan_id: int) -> Optional[Plan]:
        return self.session.get(Plan, plan_id)

    def list(self, skip: int = 0, limit: int = 100) -> list[Plan]:
        return self.session.query(Plan).offset(skip).limit(limit).all()

    def create(self, data: PlanCreate) -> Plan:
        obj = Plan(**data.dict())
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, plan_id: int, data: PlanUpdate) -> Optional[Plan]:
        obj = self.get(plan_id)
        if not obj:
            return None
        for field, value in data.dict(exclude_unset=True).items():
            setattr(obj, field, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, plan_id: int) -> bool:
        obj = self.get(plan_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True

class CompraRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, compra_id: int) -> Optional[Compra]:
        return self.session.get(Compra, compra_id)

    def get_plan(self, plan_id: int) -> Plan:
        return self.session.query(Plan).filter(Plan.id == plan_id).first()
    
    def list(self, skip: int = 0, limit: int = 100) -> list[Compra]:
        return self.session.query(Compra).offset(skip).limit(limit).all()

    def create(self, data: CompraCreate) -> Compra:
        obj = Compra(**data)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, compra_id: int, data: dict) -> Optional[Compra]:
        obj = self.get(compra_id)
        if not obj:
            return None
        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, compra_id: int) -> bool:
        obj = self.get(compra_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True

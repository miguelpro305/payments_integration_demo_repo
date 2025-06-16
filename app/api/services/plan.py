
from api.schemas.plan import PlanCreate, PlanUpdate
from database.repositories import PlanRepository


class PlanService:
    def __init__(self, repo: PlanRepository):
        self.repo = repo

    def get_plan(self, plan_id: int):
        return self.repo.get(plan_id)

    def list_plans(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def create_plan(self, data: PlanCreate):
        return self.repo.create(data)

    def update_plan(self, plan_id: int, data: PlanUpdate):
        return self.repo.update(plan_id, data)

    def delete_plan(self, plan_id: int):
        return self.repo.delete(plan_id)
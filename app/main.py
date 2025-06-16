from api.routers import compra, payment, plan
from fastapi import FastAPI

app = FastAPI(title="Payphone Integration API")

# Incluir routers
app.include_router(plan.router)
app.include_router(compra.router)
app.include_router(payment.router)
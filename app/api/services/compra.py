from datetime import datetime, timedelta
from fastapi import HTTPException
import logging
from api.models.payment import PreparePaymentRequest
from api.schemas.compra import CompraCreate, CompraUpdate
from api.services.payment import prepare_payment
from database.repositories import CompraRepository


class CompraService:
    def __init__(self, repo: CompraRepository):
        self.repo = repo

    def get_compra(self, compra_id: int):
        return self.repo.get(compra_id)

    def list_compras(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)


    async def create_compra(self, data: CompraCreate):
        # Obtener plan primero
        plan = self.repo.get_plan(data.id_plan)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan no encontrado")

        compra_data = data.model_dump()
        compra_data['estado_pago'] = 'pendiente'

        # Crear compra sin fechas aún
        compra = self.repo.create(compra_data)

        # Calcular fechas después de crear la compra
        fecha_compra = datetime.utcnow()
        fecha_finalizacion = fecha_compra + timedelta(days=plan.duracion)

        # Actualizar compra con fechas
        self.repo.update(compra.id, {
            "fecha_compra": fecha_compra,
            "fecha_finalizacion": fecha_finalizacion
        })

        try:
            payment_request = PreparePaymentRequest(
                subtotal=plan.precio,
                reference=str(compra.id)
            )
            payphone_payload = payment_request.to_payphone_payload()
            logging.info(f"Enviando a PayPhone: {payphone_payload}")
            result = await prepare_payment(payphone_payload)

            self.repo.update(compra.id, {
                "estado_pago": "En proceso",
                "id_transaccion": result["paymentId"],
                "url_pago": result["payWithCard"],
            })

            return {
                "id": compra.id,
                "id_usuario": compra.id_usuario,
                "id_plan": compra.id_plan,
                "url_pago": compra.url_pago,
                "id_transaccion": compra.id_transaccion,
                "estado_pago": compra.estado_pago,
                "fecha_compra": compra.fecha_compra,
                "fecha_finalizacion": compra.fecha_finalizacion
            }

        except Exception as e:
            logging.error(f"Error procesando pago para compra {compra.id}: {str(e)}", exc_info=True)
            self.repo.update(compra.id, {"estado_pago": "fallido"})
            raise HTTPException(status_code=500, detail="Error al iniciar el pago")


    def update_compra(self, compra_id: int, data: CompraUpdate):
        return self.repo.update(compra_id, data)

    def delete_compra(self, compra_id: int):
        return self.repo.delete(compra_id)
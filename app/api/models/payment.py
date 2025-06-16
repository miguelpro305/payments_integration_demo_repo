from pydantic import BaseModel, computed_field, field_validator, Field
import uuid
from typing import Dict, Any
from config import TAX_AMOUNT, STORE_ID, RESPONSE_URL, CURRENCY


class PreparePaymentInput(BaseModel):
    subtotal: int = Field(..., description="Monto en dólares (se convertirá a centavos)")
    reference: str = Field(..., max_length=255)


class PreparePaymentRequest(PreparePaymentInput):
    """
    Modelo final para la API de PayPhone con:
    - Conversión automática a centavos
    - Campos requeridos por PayPhone
    - Validación de valores
    """
    
    @field_validator('subtotal')
    @classmethod
    def validar_monto_positivo(cls, v: int) -> int:
        """Convierte dólares a centavos y valida que sea positivo"""
        if v <= 0:
            raise ValueError("El monto base debe ser mayor que 0")
        return v * 100  # Convertir a centavos

    @computed_field
    @property
    def tax(self) -> int:
        """Calcula el impuesto en centavos (15% del subtotal)"""
        return TAX_AMOUNT

    @computed_field
    @property
    def amountWithTax(self) -> int:
        """Monto total CON impuestos (requerido por PayPhone)"""
        return self.subtotal
    
    @computed_field
    @property
    def amount(self) -> int:
        """Total"""
        return self.subtotal + self.tax


    @computed_field
    @property
    def clientTransactionId(self) -> str:
        return f"TX-{uuid.uuid4().hex[:8]}"

    @computed_field
    @property
    def currency(self) -> str:
        return CURRENCY

    @computed_field
    @property
    def storeId(self) -> str:
        return STORE_ID

    @computed_field
    @property
    def responseUrl(self) -> str:
        return RESPONSE_URL

    def to_payphone_payload(self) -> Dict[str, Any]:
        """Formato específico que espera PayPhone"""
        return {
            "amount": self.amount,  # Monto SIN impuestos
            "amountWithTax": self.amountWithTax,
            "tax": self.tax,
            "clientTransactionId": self.clientTransactionId,
            "currency": self.currency,
            "storeId": self.storeId,
            "reference": self.reference,
            "responseUrl": self.responseUrl
        }


class ConfirmPaymentRequest(BaseModel):
    id: int = Field(..., description="ID de transacción de PayPhone")
    clientTxId: str = Field(..., description="ID único de la transacción")


    def to_payphone_payload(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "clientTxId": self.clientTxId
        }


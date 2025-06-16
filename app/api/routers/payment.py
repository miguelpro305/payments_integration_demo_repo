import logging
import httpx
from fastapi import APIRouter, HTTPException
from typing import Dict

from api.models.payment import ConfirmPaymentRequest, PreparePaymentInput, PreparePaymentRequest
from api.services.payment import prepare_confirmation, prepare_payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/start", response_model=Dict[str, str])
async def start_payment(payment_input: PreparePaymentInput):
    """
    Inicia un nuevo pago con PayPhone
    
    Args:
        payment_input: PreparePaymentInput con subtotal (en dólares) y referencia
    
    Returns:
        Dict con paymentUrl y paymentId para redirección
    """
    try:
        payment_request = PreparePaymentRequest(**payment_input.model_dump())
        payphone_payload = payment_request.to_payphone_payload()
        logging.info(f"Sending to PayPhone: {payphone_payload}")
        result = await prepare_payment(payphone_payload)
        
        return {
            "paymentUrl": result["payWithCard"],
            "paymentId": result["paymentId"]
        }
        
    except ValueError as e:
        logging.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("message", "Error processing payment")
        raise HTTPException(status_code=400, detail=f"PayPhone error: {error_detail}")
    except Exception as e:
        logging.error(f"Payment processing failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error processing payment")

@router.post("/confirm", response_model=Dict[str, str])
async def confirm_payment(confirmation: ConfirmPaymentRequest):
    """
    Confirma un pago completado en PayPhone
    
    Args:
        confirmation: ConfirmPaymentRequest con id y clientTxId
    
    Returns:
        Respuesta de confirmación de PayPhone
    """
    payphone_payload = confirmation.to_payphone_payload()
    try:
        result = await prepare_confirmation(payphone_payload)

        return {
            "email": result["email"],
            "cardType": result["cardType"],
            "bin": result["bin"],
            "lastDigits": result["lastDigits"],
            "deferredCode": result["deferredCode"],
            "deferred": str(result["deferred"]),
            "cardBrandCode": result["cardBrandCode"],
            "cardBrand": result["cardBrand"],
            "amount": str(result["amount"]),
            "clientTransactionId": result["clientTransactionId"],
            "phoneNumber": result["phoneNumber"],
            "statusCode": str(result["statusCode"]),
            "transactionStatus": result["transactionStatus"],
            "authorizationCode": result["authorizationCode"],
            "message": result["message"],
            "messageCode": str(result["messageCode"]),
            "transactionId": str(result["transactionId"]),
            "document": result["document"],
            "currency": result["currency"],
            "optionalParameter3": result["optionalParameter3"],
            "optionalParameter4": result["optionalParameter4"],
            "storeName": result["storeName"],
            "date": result["date"],
            "regionIso": result["regionIso"],
            "transactionType": result["transactionType"],
            "reference": result["reference"],
        }

    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("message", "Error confirming payment")
        logging.error(f"PayPhone confirmation error: {error_detail}")
        raise HTTPException(status_code=400, detail=f"PayPhone error: {error_detail}")
    except Exception as e:
        logging.error(f"Confirmation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail="Error confirming payment")

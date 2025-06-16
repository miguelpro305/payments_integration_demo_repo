from typing import Any, Dict
import httpx
import json
from config import CONFIRM_URL, PAYPHONE_TOKEN, PREPARE_URL


headers = {
    "Authorization": f"Bearer {PAYPHONE_TOKEN}",
    "Content-Type": "application/json"
}

async def prepare_payment(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = {
        **payload,
    }

    print("Payload que se enviará:")
    print(json.dumps(data, indent=2))
    async with httpx.AsyncClient() as client:
        response = await client.post(PREPARE_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


async def prepare_confirmation(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = {
        **payload,
    }
    print("Payload que se enviará:")
    print(json.dumps(data, indent=2))
    async with httpx.AsyncClient() as client:
        response = await client.post(CONFIRM_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

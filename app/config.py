import os
from dotenv import load_dotenv

load_dotenv()

PAYPHONE_TOKEN = os.getenv("PAYPHONE_TOKEN")
STORE_ID = os.getenv("PAYPHONE_STORE_ID")
RESPONSE_URL = os.getenv("PAYPHONE_RESPONSE_URL")
PREPARE_URL = os.getenv("PREPARE_URL")
CONFIRM_URL = os.getenv("CONFIRM_URL")
CURRENCY = os.getenv("CURRENCY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

try:
    # Default 15 si no está definido
    TAX_AMOUNT = int(os.getenv("TAX_AMOUNT", "15"))
except ValueError:
    raise ValueError(
        "TAX_AMOUNT debe ser un número entero en el .env (ej. '15')")

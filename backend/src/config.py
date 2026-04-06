import os
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_BACKEND_ROOT / ".env")


class Config:
    """Configuração carregada de variáveis de ambiente (`.env` na raiz do backend)."""

    PORT = int(os.getenv("PORT", "3333"))
    GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
    GOOGLE_SHEETS_WORKSHEET = os.getenv("GOOGLE_SHEETS_WORKSHEET", "Despesas")
    GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

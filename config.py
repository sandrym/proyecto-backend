import os
from dotenv import load_dotenv

# Carga variables desde .env si existe
load_dotenv()

FLASK_ENV = os.getenv("FLASK_ENV", "production")
FLASK_DEBUG = bool(int(os.getenv("FLASK_DEBUG", "1")))
PORT = int(os.getenv("PORT", "5000"))

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "juegosdb")
PG_USER = os.getenv("PG_USER", "alumnodb")
PG_PASSWORD = os.getenv("PG_PASSWORD", "alumnodb")

# Permitimos configurar orígenes CORS (para el frontend Vite)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")

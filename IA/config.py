import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY não encontrada. Configure a variável no .env.")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.1-flash-lite")
PETCENTER_BASE_URL = os.getenv(
    "PETCENTER_BASE_URL",
    "https://challenge-java-petcenter.onrender.com"
).rstrip("/")

# Token fixo opcional para ambientes de teste. Em produção, prefira JWT por usuário.
PETCENTER_API_TOKEN = os.getenv("PETCENTER_API_TOKEN", "").strip()
PETCENTER_USER_ID = os.getenv("PETCENTER_USER_ID", "").strip()

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Localiza e carrega o arquivo .env na pasta do projeto
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Chave de API
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError(
        "API_KEY não encontrada. Confira o arquivo .env."
    )

# Inicialização do cliente Google GenAI
client = genai.Client(api_key=API_KEY)

# URL base do servidor IoT
BASE_URL = "http://localhost:8280"

# Modelo utilizado
MODEL_NAME = "gemini-3.1-flash-lite"
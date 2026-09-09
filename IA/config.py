# -*- coding: utf-8 -*-
from google import genai

# Chave de API (substitua pela sua ou use variáveis de ambiente)
API_KEY = ""

# Inicialização do cliente Google GenAI
client = genai.Client(api_key=API_KEY)

# URL base do servidor IoT (ESP32 / Servidor Local)
BASE_URL = "http://localhost:8280"

# Nome do modelo utilizado
MODEL_NAME = "gemini-3.1-flash-lite"
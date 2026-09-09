from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import client, MODEL_NAME
from SYSTEM_PROMPT import SYSTEM_PROMPT
from tools import tools_list


app = FastAPI(
    title="CLYVO VET API",
    description="API de inteligência artificial do CLYVO VET",
    version="1.0.0"
)


# Permite que o React acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MODELOS

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# CHAT

chat = client.chats.create(
    model=MODEL_NAME,
    config={
        "system_instruction": SYSTEM_PROMPT,
        "tools": tools_list
    }
)


# ENDPOINT

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="A pergunta não pode estar vazia."
        )

    try:

        response = chat.send_message(
            request.message
        )

        return ChatResponse(
            response=response.text
        )

    except Exception as e:

        print(f"Erro: {e}")

        raise HTTPException(
            status_code=500,
            detail="Erro ao processar a pergunta."
        )
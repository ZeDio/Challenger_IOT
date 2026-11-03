from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import client, MODEL_NAME, PETCENTER_API_TOKEN, PETCENTER_USER_ID
from SYSTEM_PROMPT import SYSTEM_PROMPT
from tools import tools_list, configurar_contexto, limpar_contexto
from schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="CLYVO VET - Assistente PetCenter",
    description="Assistente de IA integrado à API Java PetCenter",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja aos domínios do frontend.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    jwt = (request.token or PETCENTER_API_TOKEN).strip()
    if not jwt:
        raise HTTPException(status_code=401, detail="Token JWT não informado. Configure PETCENTER_API_TOKEN no .env ou envie token na requisição.")

    user_id = request.user_id
    if user_id is None and PETCENTER_USER_ID.isdigit():
        user_id = int(PETCENTER_USER_ID)

    context_token = configurar_contexto(
        token=jwt,
        user_id=user_id,
        pet_id=request.pet_id
    )
    try:
        chat = client.chats.create(
            model=MODEL_NAME,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "tools": tools_list
            }
        )
        response = chat.send_message(request.message)
        answer = response.text or "Não consegui gerar uma resposta. Tente novamente."
        return ChatResponse(response=answer)
    except Exception as erro:
        print(f"Erro ao processar chat: {erro}")
        raise HTTPException(status_code=500, detail="Erro ao processar a pergunta.")
    finally:
        limpar_contexto(context_token)

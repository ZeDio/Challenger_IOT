from config import client, MODEL_NAME, PETCENTER_API_TOKEN, PETCENTER_USER_ID
from SYSTEM_PROMPT import SYSTEM_PROMPT
from tools import tools_list, configurar_contexto, limpar_contexto

def interagir_com_clyvo_vet():
    print("\n--- CLYVO VET / PetCenter ---")
    token = PETCENTER_API_TOKEN or input("JWT do PetCenter: ").strip()
    if PETCENTER_API_TOKEN:
        print("Usando JWT configurado no .env.")
    # O ID do tutor será descoberto automaticamente pelo email (sub) do JWT.
    # PETCENTER_USER_ID continua opcional apenas para testes/compatibilidade.
    user_id = PETCENTER_USER_ID.strip() if PETCENTER_USER_ID else ""
    pet_id = input("ID do pet padrão (opcional): ").strip()

    context_token = configurar_contexto(
        token,
        int(user_id) if user_id.isdigit() else None,
        int(pet_id) if pet_id else None
    )
    try:
        chat = client.chats.create(
            model=MODEL_NAME,
            config={"system_instruction": SYSTEM_PROMPT, "tools": tools_list}
        )
        print("Assistente iniciado. Digite 'sair' para encerrar.")
        while True:
            pergunta = input("\nVocê: ").strip()
            if pergunta.lower() in ("sair", "encerrar", "parar"):
                print("CLYVO VET: Até a próxima!")
                break
            if not pergunta:
                continue
            try:
                resposta = chat.send_message(pergunta)
                print(f"CLYVO VET: {resposta.text}")
            except Exception as erro:
                print(f"Erro no processamento: {erro}")
    finally:
        limpar_contexto(context_token)

if __name__ == "__main__":
    interagir_com_clyvo_vet()

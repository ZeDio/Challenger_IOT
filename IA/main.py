import time
from config import client, MODEL_NAME
from SYSTEM_PROMPT import SYSTEM_PROMPT
from tools import tools_list
from schemas import FichaMonitoramento

# CONFIGURAÇÃO DO CHAT
chat = client.chats.create(
    model=MODEL_NAME,
    config={
        "system_instruction": SYSTEM_PROMPT,
        "tools": tools_list
    }
)

def interagir_com_clyvo_vet():
    print(
        "\n--- Assistente CLYVO VET iniciado "
        "(Digite 'sair' para encerrar) ---\n"
    )

    print(
        "CLYVO VET: Olá! Sou o assistente CLYVO VET. "
        "Como posso ajudar com o seu pet?"
    )
 
    # LOOP PRINCIPAL DO CHAT
    while True:
        user_input = input("\nVocê: ").strip()
 
        # ENCERRAMENTO
        if user_input.lower() in ["sair", "encerrar", "parar"]:
            print("CLYVO VET: Atendimento encerrado. Até a próxima!")
            break
 
        # IGNORA ENTRADAS VAZIAS
        if not user_input:
            print(
                "CLYVO VET: Por favor, envie uma pergunta "
                "sobre alimentação ou hidratação do pet."
            )
            continue

        try:
            # ENVIA A PERGUNTA PARA O MODELO
            response = chat.send_message(user_input)
 
            # RESPOSTA DO ASSISTENTE
            print(f"CLYVO VET: {response.text}")
 
            # VERIFICA SE A CONSULTA ESTÁ FORA DO ESCOPO
            texto_resposta = response.text.lower()
            if (
                "fora do escopo" in texto_resposta
                or "não posso ajudar" in texto_resposta
                or "não posso responder" in texto_resposta
            ):
                print(
                    "\n[INFO] A solicitação não pertence "
                    "ao escopo do CLYVO VET.\n"
                )
                continue
 
            # GERAÇÃO DA FICHA ESTRUTURADA
            palavras_ficha = [
                "consulta concluída",
                "dados do monitoramento",
                "monitoramento realizado",
                "consulta realizada"
            ]
            gerar_ficha = any(
                palavra in texto_resposta
                for palavra in palavras_ficha
            )
 
            if gerar_ficha:
                print(
                    "\n--- [SISTEMA] Gerando dados estruturados "
                    "via Pydantic... ---"
                )
 
                # TRANSFORMA A RESPOSTA EM JSON
                final_data_response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=f"""
                    Gere um JSON rigoroso baseado exclusivamente
                    nos dados presentes nesta resposta do CLYVO VET.
 
                    NÃO invente informações.
 
                    Resposta do assistente:
                    {response.text}
                    """,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": FichaMonitoramento
                    }
                )
 
                # OBJETO PYDANTIC VALIDADO
                ficha = final_data_response.parsed
                print("\n✅ JSON VALIDADO COM SUCESSO:")
                print(
                    ficha.model_dump_json(
                        indent=2,
                        ensure_ascii=False
                    )
                )
                print(
                    "--- [SISTEMA] Consulta registrada "
                    "com sucesso. ---\n"
                )
 
        # TRATAMENTO DE ERROS
        except Exception as e:
            if "503" in str(e):
                print(
                    "CLYVO VET: O sistema está temporariamente "
                    "indisponível. Tente novamente em alguns "
                    "segundos."
                )
                time.sleep(2)
            else:
                print(f"Erro no processamento: {e}")

if __name__ == "__main__":
    interagir_com_clyvo_vet()
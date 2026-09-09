# -*- coding: utf-8 -*-
"""
CLYVO VET Challenger

Original file is located at
    https://colab.research.google.com/drive/1uQOtW1o4nlOGtkVi7hAWlylnQ0dQWuv4
"""
 
''' 
    pip install -q -U "google-genai>=2.3.0" "pydantic>=2.0" 

    Rodar esse comando antes de começar a rodar o codigo
'''

import requests
import time
from google import genai
from SYSTEM_PROMPT import SYSTEM_PROMPT
from typing import Literal, Optional
from pydantic import BaseModel, Field
 
api_key = ""
client = genai.Client(api_key=api_key)

 
class ConsultaCLYVOVET(BaseModel):
    # TIPO DE INFORMAÇÃO SOLICITADA
    tipo_consulta: Literal[
        "status",
        "comida",
        "agua",
        "historico"
    ] = Field(
        description=(
            "Tipo de informação que o usuário deseja consultar. "
            "Use 'status' para informações gerais de alimentação e hidratação, "
            "'comida' para informações sobre refeições, "
            "'agua' para informações sobre hidratação, "
            "'historico' para consultar informações de dias anteriores."
        )
    )
 
    # DATA DA CONSULTA
    data: Optional[str] = Field(
        default=None,
        description=(
            "Data que o usuário deseja consultar no formato DD/MM/YYYY. "
            "Se o usuário não informar uma data, considerar o dia atual."
        )
    )
 
    # TIPO DE DADO SOLICITADO
    informacao_solicitada: Literal[
        "quantidade",
        "horarios",
        "ultimo_evento",
        "primeiro_evento",
        "resumo"
    ] = Field(
        description=(
            "Tipo de informação solicitada pelo usuário. "
            "'quantidade' retorna o número de eventos, "
            "'horarios' retorna os horários registrados, "
            "'ultimo_evento' retorna o horário do último evento, "
            "'primeiro_evento' retorna o horário do primeiro evento, "
            "'resumo' retorna um resumo geral."
        )
    )
 
    # CONTROLE DE ESCOPO
    dentro_do_escopo: bool = Field(
        description=(
            "Indica se a solicitação do usuário está relacionada "
            "ao monitoramento IoT do CLYVO VET."
        )
    )
 
    # CONTROLE DA CONSULTA
    precisa_esclarecimento: bool = Field(
        description=(
            "Indica se é necessário solicitar alguma informação "
            "adicional ao usuário antes de realizar a consulta."
        )
    )
 
    pergunta_esclarecimento: Optional[str] = Field(
        default=None,
        description=(
            "Pergunta objetiva para obter a informação que está faltando. "
            "Use apenas quando precisa_esclarecimento for True."
        )
    )
 
    # RESPOSTA ESPERADA
    resposta_esperada: str = Field(
        description=(
            "Descrição objetiva do que o agente deve retornar ao usuário "
            "após consultar os dados do IoT."
        )
    );

 
BASE_URL = "http://localhost:8280"
 
 
def consultar_status() -> dict:
    """
    Consulta o status atual do monitoramento do pet.
    GET /status
    """
    try:
        resposta = requests.get(
            f"{BASE_URL}/status",
            timeout=5
        )
 
        resposta.raise_for_status()
 
        return resposta.json()
 
    except requests.RequestException as erro:
        return {
            "erro": f"Não foi possível consultar o status: {erro}"
        }
 
 
def consultar_comida(data: Optional[str] = None) -> dict:
    """
    Consulta os eventos relacionados à alimentação do pet.
 
    GET /comida
 
    Args:
        data: Data desejada no formato DD/MM/YYYY.
              Atualmente o ESP32 retorna os dados do dia atual.
    """
 
    try:
        resposta = requests.get(
            f"{BASE_URL}/comida",
            timeout=5
        )
 
        resposta.raise_for_status()
 
        dados = resposta.json()
 
        # Se foi solicitada uma data específica,
        # podemos verificar a data retornada pela API.
        if data is not None and dados.get("data") != data:
            return {
                "erro": f"Não existem dados para a data {data}"
            }
 
        return dados
 
    except requests.RequestException as erro:
        return {
            "erro": f"Não foi possível consultar alimentação: {erro}"
        }
 
 
def consultar_agua(data: Optional[str] = None) -> dict:
    """
    Consulta os eventos relacionados à hidratação do pet.
 
    GET /agua
 
    Args:
        data: Data desejada no formato DD/MM/YYYY.
              Atualmente o ESP32 retorna os dados do dia atual.
    """
 
    try:
        resposta = requests.get(
            f"{BASE_URL}/agua",
            timeout=5
        )
 
        resposta.raise_for_status()
 
        dados = resposta.json()
 
        if data is not None and dados.get("data") != data:
            return {
                "erro": f"Não existem dados para a data {data}"
            }
 
        return dados
 
    except requests.RequestException as erro:
        return {
            "erro": f"Não foi possível consultar hidratação: {erro}"
        }
 
 
def consultar_historico() -> dict:
    """
    Consulta o histórico diário de alimentação e hidratação.
 
    GET /historico
    """
 
    try:
        resposta = requests.get(
            f"{BASE_URL}/historico",
            timeout=5
        )
 
        resposta.raise_for_status()
 
        return resposta.json()
 
    except requests.RequestException as erro:
        return {
            "erro": f"Não foi possível consultar histórico: {erro}"
        }
 
 
# Lista de ferramentas disponíveis para o modelo
tools_list = [
    consultar_status,
    consultar_comida,
    consultar_agua,
    consultar_historico
]
 
 
class FichaMonitoramento(BaseModel):
    nome_pet: str
    tipo_consulta: Literal[
        "status",
        "comida",
        "agua",
        "historico"
    ]
 
    data: Optional[str] = None
    informacao_solicitada: Literal[
        "quantidade",
        "horarios",
        "ultimo_evento",
        "primeiro_evento",
        "resumo"
    ]
 
    visitas_comida: Optional[int] = None
    visitas_agua: Optional[int] = None
    horarios_comida: Optional[list[str]] = None
    horarios_agua: Optional[list[str]] = None
    resposta: str
 
 
# CONFIGURAÇÃO DO CHAT
MODEL_NAME = "gemini-3.1-flash-lite"
 
chat = client.chats.create(
    model=MODEL_NAME,
    config={
        "system_instruction": SYSTEM_PROMPT,
        "tools": tools_list
    }
)
 
# INTERAÇÃO COM O CLYVO VET
def interagir_com_clyvo_vet():

    print(
        "\n--- Assistente CLYVO VET iniciado "
        "(Digite 'sair' para encerrar) ---\n"
    )

    print(
        "CLYVO VET: Olá! Sou o assistente CLYVO VET. "
        "Como posso ajudar com o seu pet?"
    )

    while True:
        user_input = input("\nVocê: ").strip()

        if user_input.lower() in {
            "sair",
            "encerrar",
            "parar"
        }:
            print(
                "CLYVO VET: Até a próxima!"
            )
            break

        if not user_input:
            continue

        try:
            response = chat.send_message(user_input)

            print(f"CLYVO VET: {response.text}")

        except Exception as e:
            if "503" in str(e):
                print(
                    "CLYVO VET: O serviço está temporariamente "
                    "indisponível. Tente novamente em alguns segundos."
                )
                time.sleep(2)
            else:
                print(f"Erro no processamento: {e}")
    print(
        "--- Assistente CLYVO VET iniciado "
        "(Digite 'sair' para encerrar) ---"
    )
 
    # SAUDAÇÃO INICIAL
    try:
 
        primeira_resposta = chat.send_message(
            "Olá! Por favor, apresente-se como assistente "
            "CLYVO VET e explique brevemente como pode ajudar "
            "com o monitoramento de alimentação e hidratação."
        )
        print(f"CLYVO VET: {primeira_resposta.text}")
 
    except Exception as e:
        print(
            f"Erro ao conectar com o servidor: {e}. "
            "Tente executar novamente."
        )
        return
 
    # LOOP PRINCIPAL DO CHAT
    while True:
        user_input = input("\nVocê: ").strip()
 
        # ENCERRAMENTO
        if user_input.lower() in [
            "sair",
            "encerrar",
            "parar"
        ]:
 
            print(
                "CLYVO VET: Atendimento encerrado. "
                "Até a próxima!"
            )
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
                print(
                    "\n✅ JSON VALIDADO COM SUCESSO:"
                )
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
                print(
                    f"Erro no processamento: {e}"
                )
 
# INICIAR O CHAT
interagir_com_clyvo_vet()
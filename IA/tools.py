from typing import Optional
import requests
from config import BASE_URL

def consultar_status() -> dict:
    """
    Consulta o status atual do monitoramento do pet.
    GET /status
    """
    try:
        resposta = requests.get(f"{BASE_URL}/status", timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as erro:
        return {"erro": f"Não foi possível consultar o status: {erro}"}


def consultar_comida(data: Optional[str] = None) -> dict:
    """
    Consulta os eventos relacionados à alimentação do pet.
    GET /comida
    """
    try:
        resposta = requests.get(f"{BASE_URL}/comida", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
 
        if data is not None and dados.get("data") != data:
            return {"erro": f"Não existem dados para a data {data}"}
 
        return dados
    except requests.RequestException as erro:
        return {"erro": f"Não foi possível consultar alimentação: {erro}"}


def consultar_agua(data: Optional[str] = None) -> dict:
    """
    Consulta os eventos relacionados à hidratação do pet.
    GET /agua
    """
    try:
        resposta = requests.get(f"{BASE_URL}/agua", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
 
        if data is not None and dados.get("data") != data:
            return {"erro": f"Não existem dados para a data {data}"}
 
        return dados
    except requests.RequestException as erro:
        return {"erro": f"Não foi possível consultar hidratação: {erro}"}


def consultar_historico() -> dict:
    """
    Consulta o histórico diário de alimentação e hidratação.
    GET /historico
    """
    try:
        resposta = requests.get(f"{BASE_URL}/historico", timeout=5)
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException as erro:
        return {"erro": f"Não foi possível consultar histórico: {erro}"}


# Lista de ferramentas disponíveis para o modelo
tools_list = [
    consultar_status,
    consultar_comida,
    consultar_agua,
    consultar_historico
]
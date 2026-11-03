from contextvars import ContextVar
from typing import Optional
import base64
import json
from urllib.parse import quote
import requests
from config import PETCENTER_BASE_URL

# Contexto isolado por requisição: evita compartilhar JWT entre usuários.
_request_context = ContextVar("petcenter_request_context", default={})

def configurar_contexto(token: str, user_id: Optional[int] = None, pet_id: Optional[int] = None):
    return _request_context.set({
        "token": token,
        "user_id": user_id,
        "pet_id": pet_id
    })

def limpar_contexto(context_token):
    _request_context.reset(context_token)

def _get(path: str, params: Optional[dict] = None):
    context = _request_context.get()
    token = context.get("token")
    if not token:
        return {"erro": "Token JWT não informado. Faça login e envie o token no cabeçalho Authorization."}
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        response = requests.get(
            f"{PETCENTER_BASE_URL}{path}",
            headers=headers,
            params=params or {},
            timeout=20
        )
        if response.status_code == 401:
            return {"erro": "Sessão expirada ou token inválido. Faça login novamente."}
        if response.status_code == 403:
            return {"erro": "O usuário não possui permissão para consultar esses dados."}
        response.raise_for_status()
        return response.json() if response.content else {"mensagem": "Consulta realizada sem conteúdo."}
    except requests.RequestException as erro:
        return {"erro": f"Falha ao consultar a API PetCenter: {erro}"}
    except ValueError:
        return {"erro": "A API PetCenter retornou uma resposta que não está em JSON."}

def _email_do_token(token: str):
    """Extrai o subject (email) do payload JWT. A validação real é feita pela API Java."""
    try:
        partes = token.split(".")
        if len(partes) != 3:
            return None
        payload = partes[1]
        payload += "=" * (-len(payload) % 4)
        dados = json.loads(base64.urlsafe_b64decode(payload.encode("utf-8")))
        email = dados.get("sub")
        return email if isinstance(email, str) and email.strip() else None
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def _resolver_user_id():
    """Obtém o ID pelo email do JWT usando GET /api/users/email/{email}."""
    context = _request_context.get()
    user_id = context.get("user_id")
    if user_id is not None:
        return user_id

    token = context.get("token")
    if not token:
        return {"erro": "Token JWT não informado."}

    email = _email_do_token(token)
    if not email:
        return {"erro": "Não foi possível identificar o email (sub) no JWT."}

    usuario = _get(f"/api/users/email/{quote(email, safe='')}")
    if isinstance(usuario, dict) and usuario.get("erro"):
        return usuario
    user_id = usuario.get("id") if isinstance(usuario, dict) else None
    if user_id is None:
        return {"erro": "A API Java não retornou o ID do usuário."}

    # Guarda o ID apenas no contexto desta execução/conversa.
    context_atualizado = dict(context)
    context_atualizado["user_id"] = int(user_id)
    _request_context.set(context_atualizado)
    return int(user_id)


def consultar_meus_pets():
    """Lista os pets do usuário identificado automaticamente pelo JWT."""
    user_id = _resolver_user_id()
    if isinstance(user_id, dict):
        return user_id
    return _get(f"/api/pets/user/{user_id}", {"page": 0, "size": 100})

def consultar_pet(pet_id: Optional[int] = None):
    """Consulta os dados cadastrais de um pet pelo identificador."""
    pet_id = pet_id or _request_context.get().get("pet_id")
    if pet_id is None:
        return {"erro": "Informe qual pet deseja consultar (pet_id)."}
    return _get(f"/api/pets/{pet_id}")

def consultar_diarios(data: Optional[str] = None):
    """Consulta o diário do pet. Informe data no formato aceito pela API, se desejar filtrar por dia."""
    if data:
        return _get(f"/api/diarioentradas/data/{data}", {"page": 0, "size": 100})
    return _get("/api/diarioentradas", {"page": 0, "size": 100})

def consultar_veterinarios_do_pet(pet_id: Optional[int] = None):
    """Lista os veterinários associados a um pet."""
    pet_id = pet_id or _request_context.get().get("pet_id")
    if pet_id is None:
        return {"erro": "Informe qual pet deseja consultar (pet_id)."}
    return _get(f"/api/pet-veterinarios/pet/{pet_id}")

def consultar_alertas_do_pet(pet_id: Optional[int] = None):
    """Consulta os alertas disponíveis para um pet."""
    pet_id = pet_id or _request_context.get().get("pet_id")
    if pet_id is None:
        return {"erro": "Informe qual pet deseja consultar (pet_id)."}
    return _get(f"/api/alertas/pet/{pet_id}")

def consultar_solicitacoes():
    """Consulta as solicitações de atendimento veterinário disponíveis para o usuário autenticado."""
    return _get("/api/solicitacoes", {"page": 0, "size": 100})

tools_list = [
    consultar_meus_pets,
    consultar_pet,
    consultar_diarios,
    consultar_veterinarios_do_pet,
    consultar_alertas_do_pet,
    consultar_solicitacoes,
]

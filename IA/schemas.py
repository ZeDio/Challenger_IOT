from typing import Optional, Literal
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    token: Optional[str] = Field(None, description="JWT opcional; se omitido, usa PETCENTER_API_TOKEN do .env.")
    user_id: Optional[int] = None
    pet_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str

class PetCenterPet(BaseModel):
    id: Optional[int] = None
    nomeTutor: Optional[str] = None
    nome: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    dataNascimento: Optional[str] = None
    observacoes: Optional[str] = None

class PetCenterDiarioEntrada(BaseModel):
    id: Optional[int] = None
    idPet: Optional[int] = None
    nomePet: Optional[str] = None
    data: Optional[str] = None
    resumo: Optional[str] = None
    humorGeral: Optional[str] = None
    status: Optional[Literal["COMPLETO", "PARCIAL", "VAZIO"]] = None
    criadoEm: Optional[str] = None
    atualizadoEm: Optional[str] = None

class PetCenterRegistro(BaseModel):
    id: Optional[int] = None
    idDiarioEntrada: Optional[int] = None
    tipo: Optional[str] = None
    subtipo: Optional[str] = None
    valor: Optional[str] = None
    unidade: Optional[str] = None
    nota: Optional[str] = None
    horario: Optional[str] = None
    atualizadoEm: Optional[str] = None

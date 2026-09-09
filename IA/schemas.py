# -*- coding: utf-8 -*-
from typing import Literal, Optional
from pydantic import BaseModel, Field

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
    )


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
# CLYVO VET — Assistente integrado ao PetCenter

Esta versão substitui as consultas ao ESP32/IoT pela API Java Spring Boot PetCenter. O Gemini continua sendo o modelo de linguagem e o FastAPI continua expondo o endpoint `/chat`.

## Arquitetura

React → FastAPI (Python) → Gemini + ferramentas → API Java PetCenter → banco de dados

O Gemini não acessa o banco de dados diretamente. As ferramentas Python consultam a API Java e devolvem os resultados ao modelo.

## Configuração

1. Instale Python 3.10+.
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env`.
4. Preencha `API_KEY` com sua chave do Google Gemini.
5. Confira `PETCENTER_BASE_URL`.
6. Se o frontend não enviar JWT, preencha `PETCENTER_API_TOKEN` com um token válido no `.env` (não compartilhe nem publique esse arquivo). Se usar token fixo, informe também `PETCENTER_USER_ID` para listar os pets do tutor.

## Executar

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

A documentação FastAPI fica em `/docs` e a verificação de disponibilidade em `/health`.

## Requisição do chat

O frontend pode enviar o JWT recebido no login do PetCenter, sem o prefixo `Bearer`, além do identificador do usuário. Alternativamente, em testes, configure `PETCENTER_API_TOKEN` no `.env` e deixe `token` de fora da requisição. O `pet_id` é opcional quando a pergunta se refere a um pet específico já selecionado.

```json
{
  "message": "Quais pets estão cadastrados para mim?",
  "user_id": 123,
  "pet_id": 456
}
```

O backend encaminha o token à API Java como `Authorization: Bearer <token>`. Quando recebido do frontend, o token é isolado por requisição. O token fixo do `.env` é uma alternativa apenas para testes/uso de um único usuário; todas as chamadas usarão a identidade e as permissões desse token.

## Ferramentas integradas

| Ferramenta | Endpoint Java |
|---|---|
| Listar pets do tutor | `GET /api/pets/user/{userId}` |
| Consultar pet | `GET /api/pets/{id}` |
| Consultar diário | `GET /api/diarioentradas` |
| Diário por data | `GET /api/diarioentradas/data/{data}` |
| Veterinários do pet | `GET /api/pet-veterinarios/pet/{petId}` |
| Alertas do pet | `GET /api/alertas/pet/{petId}` |
| Solicitações | `GET /api/solicitacoes` |

As listas são consultadas com `page=0` e `size=100`. Se a API retornar paginação com mais páginas, esta implementação ainda não percorre automaticamente todas elas.

## Login

O login continua sendo responsabilidade do frontend/API Java:

`POST /api/auth/login`

Corpo esperado: `email` e `senha`. O frontend deve guardar o token recebido e enviá-lo no corpo da chamada `/chat`. Não envie senha do usuário para o Gemini.

## Limitações conhecidas

- A documentação disponível não apresentou endpoint específico para agenda ou consultas veterinárias marcadas. A ferramenta de solicitações consulta pedidos de atendimento, que não devem ser apresentados como consultas agendadas.
- O diário fornece registros informados na plataforma; não são diagnósticos clínicos.
- Os endpoints de alertas, diário e solicitações devem ser validados com um JWT real e dados de teste no ambiente PetCenter.
- O `user_id` e o `pet_id` devem vir do estado autenticado/seleção do frontend, nunca de valores inventados pelo modelo.
- O CORS está aberto para facilitar o desenvolvimento. Em produção, restrinja `allow_origins` ao domínio do frontend.

## Observação sobre continuidade da conversa

O endpoint `/chat` cria um contexto Gemini por requisição para não misturar conversas ou tokens de usuários diferentes. Assim, o histórico conversacional não é mantido automaticamente entre chamadas. Se o frontend precisar de memória de conversa, deverá enviar o histórico de mensagens em cada requisição e a API deverá ser estendida para reconstruí-lo.


### Identificação automática do tutor

O `tools.py` lê o campo `sub` do payload JWT (email) e consulta `GET /api/users/email/{email}` usando o mesmo Bearer Token. A API Java valida a assinatura/permissões e retorna o `id` do próprio usuário autenticado. Esse ID é então usado em `GET /api/pets/user/{userId}`. Não é necessário preencher `PETCENTER_USER_ID` para esse fluxo.

O payload do JWT é decodificado no Python apenas para descobrir o email; isso **não substitui a validação criptográfica**. A validação de verdade continua sendo feita pelo backend Java ao receber o token.

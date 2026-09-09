# 🐾 CLYVO VET — Assistente Virtual

Assistente de chat via terminal desenvolvido pela **Code & Paws** para o **CLYVO VET**, uma plataforma de acompanhamento contínuo da saúde e rotina de pets (o "Diário Inteligente do Pet").

Nesta versão, o assistente consulta em linguagem natural os dados coletados por um sistema **IoT** (ESP32 + sensores ultrassônicos HC-SR04) que monitora as visitas do pet aos recipientes de **comida** e **água**, e também oferece orientações gerais e seguras sobre bem-estar do animal — sem nunca inventar dados nem fazer diagnósticos veterinários.

## Como funciona

- O usuário conversa livremente pelo terminal ("Quantas vezes meu cachorro comeu hoje?", "Que horas ele bebeu água?", etc).
- O modelo (Gemini) interpreta a pergunta e, quando necessário, chama automaticamente uma das ferramentas em `tools.py`, que fazem requisições HTTP para a API REST do ESP32:
  - `consultar_status()` → `GET /status`
  - `consultar_comida()` → `GET /comida`
  - `consultar_agua()` → `GET /agua`
  - `consultar_historico()` → `GET /historico`
- Quando a consulta é concluída, o sistema gera automaticamente uma ficha estruturada e validada em JSON (via Pydantic) com os dados do monitoramento.
- Todo o comportamento, tom de voz e regras de escopo do assistente estão definidos em `SYSTEM_PROMPT.py`.

## Estrutura do projeto

```
├── main.py           # Ponto de entrada — inicia o chat no terminal
├── config.py          # Configuração do cliente Gemini (API key, URL do IoT, modelo)
├── SYSTEM_PROMPT.py    # Prompt de sistema com todas as regras do assistente
├── schemas.py          # Modelos Pydantic (validação de dados/JSON estruturado)
└── tools.py            # Funções que consultam a API do ESP32/IoT
```

> ⚠️ **Importante:** este assistente é só a "camada de conversa" do CLYVO VET. Ele **não funciona sozinho** — ele consulta os dados via HTTP em `BASE_URL` (`http://localhost:8280`), então a parte de **IoT (ESP32)** precisa estar rodando e expondo a API REST **antes** de você iniciar o `main.py`. Sem isso, as ferramentas em `tools.py` vão retornar erro de conexão.

## Pré-requisitos

- **Python 3.10+** instalado na máquina
- Uma **chave de API do Google Gemini** (API key)
- **Visual Studio Code** + extensão **Wokwi** (para simular o ESP32) — ou o hardware físico (ESP32 + sensores HC-SR04 + LCD I2C) já montado e gravado com o firmware
- Git (opcional, para clonar o repositório)

## 1. Rodar a parte do IoT (ESP32) no VS Code com a extensão Wokwi

O assistente depende dos dados que o ESP32 disponibiliza pela API REST, e essa simulação roda **dentro do próprio VS Code**, através da extensão Wokwi. Antes de tudo:

1. Instale a extensão **Wokwi for VS Code** na aba de extensões do VS Code (ícone de peças no menu lateral, buscar por "Wokwi").
2. Ative a licença gratuita da extensão, se solicitado (a Wokwi pede um cadastro simples na primeira vez que você usa).
3. Abra a pasta do firmware/simulação no VS Code (**File → Open Folder**) — ela deve conter os arquivos `diagram.json`, `wokwi.toml` e o `sketch.ino` (ou `.cpp`) do ESP32.
4. Inicie a simulação de uma das formas:
   - Abra o arquivo `diagram.json` e clique no botão **▶ Start Simulation** que aparece no canto superior direito; **ou**
   - Pressione `F1` (ou `Ctrl+Shift+P` / `Cmd+Shift+P`), digite `Wokwi: Start Simulator` e pressione Enter.
5. A simulação abre em uma aba própria do VS Code, mostrando o ESP32, os sensores, o LCD e o Serial Monitor rodando ali mesmo.
6. Acompanhe pelo Serial Monitor / display LCD até o ESP32 conectar ao Wi-Fi e exibir o IP local — é nesse endereço que a API REST (`/status`, `/comida`, `/agua`, `/historico`) fica disponível.
7. **Deixe essa aba da simulação aberta e rodando** dentro do VS Code — ela precisa continuar ativa em segundo plano enquanto você usa o assistente Python.

> Se estiver usando o hardware físico real (em vez do Wokwi), ou se a simulação expor um IP/porta diferente de `localhost:8280`, anote o endereço — você vai precisar dele no próximo passo.

## 2. Instalar e configurar o Assistente Virtual (Python)

Com a simulação do Wokwi rodando, abra um **novo terminal** no VS Code (**Terminal → New Terminal**, sem fechar a simulação) para preparar o assistente Python:

1. Clone ou baixe os arquivos do projeto do assistente.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure sua chave de API. Abra o arquivo `config.py` e insira sua chave:

```python
API_KEY = "SUA_CHAVE_AQUI"
```

> 💡 Recomendado: em vez de deixar a chave direto no código, use uma variável de ambiente (`os.environ["GEMINI_API_KEY"]`) para não expor a chave caso o projeto seja compartilhado ou versionado no Git.

4. Ajuste `BASE_URL` em `config.py` para o endereço real do seu ESP32/Wokwi (o IP mostrado no LCD/Serial Monitor no passo 1), caso não seja o padrão:

```python
BASE_URL = "http://localhost:8280"
```

## 3. Executar o Assistente

Nesse mesmo terminal do VS Code, com a simulação Wokwi **ainda rodando** em outra aba, as dependências instaladas e a API key configurada, execute:

```bash
python main.py
```

O chat será iniciado no terminal:

```
--- Assistente CLYVO VET iniciado (Digite 'sair' para encerrar) ---

CLYVO VET: Olá! Sou o assistente CLYVO VET. Como posso ajudar com o seu pet?
```

Basta digitar sua pergunta e pressionar Enter. Para encerrar, digite `sair`, `encerrar` ou `parar`.

## Fluxo completo

```
Abrir o projeto no VS Code
        ↓
Instalar extensão Wokwi e iniciar a simulação (F1 → Wokwi: Start Simulator)
        ↓
ESP32 conecta ao Wi-Fi e expõe a API REST
        ↓
Abrir novo terminal no VS Code (sem fechar a simulação)
        ↓
Instalar dependências Python
        ↓
Configurar API Key e BASE_URL
        ↓
Rodar python main.py
        ↓
Fazer perguntas ao CLYVO VET
```

## Exemplos de perguntas

- "Quantas vezes meu pet comeu hoje?"
- "Que horas ele bebeu água?"
- "Mostre o histórico dos últimos dias."
- "Ele comeu mais ontem ou hoje?"
- "Como posso incentivar meu cachorro a beber mais água?"

## Limitações importantes

- O assistente **nunca inventa dados**: se o IoT não retornar informação, ele avisa que não há registros.
- O assistente **não realiza diagnósticos veterinários** e sempre recomenda a busca por um profissional em casos de saúde ou sofrimento do animal.
- Perguntas totalmente fora do contexto de pets/CLYVO VET são recusadas de forma breve.
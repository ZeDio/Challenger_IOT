# 🐾 Challenger IoT — CLYVO VET

Sistema IoT inteligente para monitoramento alimentar e de hidratação de pets utilizando ESP32, sensores ultrassônicos, display LCD I2C e API REST em JSON.

---

# 📖 Sobre o Projeto

O **CLYVO VET** foi desenvolvido com o objetivo de auxiliar tutores e profissionais veterinários no acompanhamento do comportamento alimentar e da hidratação de animais domésticos.

O sistema monitora automaticamente quando o pet:
- se aproxima do recipiente de comida
- se aproxima do recipiente de água

Cada evento é registrado em tempo real, armazenando:
- quantidade de visitas
- horário exato do evento
- tipo da interação

Além disso, os dados são disponibilizados através de uma API REST em JSON, permitindo integração com:
- dashboards
- aplicativos
- sistemas veterinários
- plataformas IoT

---

# 🎯 Objetivo

O projeto busca transformar ações simples do cotidiano em dados relevantes para análise comportamental e prevenção de problemas de saúde.

Muitos tutores:
- não acompanham a rotina do pet
- não percebem alterações de comportamento rapidamente
- não possuem histórico de alimentação e hidratação

O CLYVO VET resolve isso automatizando todo o monitoramento.

---

# 💡 Funcionalidades

✅ Monitoramento de alimentação  
✅ Monitoramento de hidratação  
✅ Registro de horário via NTP  
✅ Display LCD em tempo real  
✅ API REST em JSON  
✅ Integração via Wi-Fi  
✅ Botões físicos para visualização dos dados no Serial Monitor  
✅ Sistema embarcado utilizando ESP32  

---

# 🧠 Funcionamento do Sistema

O sistema utiliza dois sensores ultrassônicos HC-SR04:

- um sensor monitora a área da comida
- outro sensor monitora a área da água

Quando o pet aproxima do recipiente:
1. o sensor detecta redução da distância
2. o ESP32 identifica a presença
3. o sistema registra o horário via NTP
4. os contadores são atualizados
5. o LCD exibe o evento
6. os dados ficam disponíveis na API REST

---

# 🖼️ Preview do Projeto

![Projeto IoT](./Projeto_IOT.png)

---

# 🔧 Tecnologias Utilizadas

## Hardware

- ESP32
- 2x Sensores HC-SR04
- LCD I2C 16x2
- Protoboard
- Botões físicos
- Jumpers

---

## Software

- Arduino C++
- ESP32 WiFi
- WebServer
- NTP
- Wokwi
- LCD I2C

---

# ⚙️ Componentes e Pinos

## Sensores

### Sensor de Comida

| Componente | Pino ESP32 |
|---|---|
| TRIG | GPIO 5 |
| ECHO | GPIO 18 |

---

### Sensor de Água

| Componente | Pino ESP32 |
|---|---|
| TRIG | GPIO 15 |
| ECHO | GPIO 2 |

---

## LCD I2C

| LCD | ESP32 |
|---|---|
| SDA | GPIO 21 |
| SCL | GPIO 22 |
| VCC | 3V3 |
| GND | GND |

---

## Botões

| Botão | Pino |
|---|---|
| STATUS | GPIO 13 |
| ÁGUA | GPIO 12 |
| COMIDA | GPIO 14 |

---

# 🌐 API REST

O ESP32 cria um servidor HTTP local disponibilizando os dados do sistema em formato JSON.

---

# 📡 Endpoint `/status`

Retorna o resumo geral do sistema.

## Exemplo

```json
{
  "visitasComida": 5,
  "visitasAgua": 3
}
```

---

# 🍖 Endpoint `/comida`

Retorna:
- quantidade de visitas à comida
- horários registrados

## Exemplo

```json
{
  "visitasComida": 5,
  "visitaHorario": [
    "08:10:22",
    "12:40:11"
  ]
}
```

---

# 💧 Endpoint `/agua`

Retorna:
- quantidade de visitas à água
- horários registrados

## Exemplo

```json
{
  "visitasAgua": 3,
  "visitaHorario": [
    "09:14:55",
    "13:02:10"
  ]
}
```

---

# 🖥️ Interface LCD

O display LCD apresenta informações em tempo real durante toda execução do sistema.

---

## Inicialização

```text
Iniciando...
```

---

## Conexão Wi-Fi

```text
Conectando
WiFi...
```

---

## Wi-Fi conectado

```text
WiFi conectado
```

---

## Exibição do IP

```text
IP:
192.168.x.x
```

---

## Tela principal

```text
Refeicoes: X
Hidratacao: X
```

---

## Evento de alimentação

```text
Pet comeu!
12:40:22
```

---

## Evento de hidratação

```text
Bebeu agua!
13:10:11
```

---

# 🔘 Botões Físicos

O sistema possui três botões físicos conectados ao ESP32.

Cada botão imprime um JSON específico no Serial Monitor.

---

## Botão STATUS — GPIO 13

Exibe:

```json
{
  "visitasComida": 5,
  "visitasAgua": 3
}
```

---

## Botão ÁGUA — GPIO 12

Exibe:

```json
{
  "visitasAgua": 3,
  "visitaHorario": [
    "09:14:55",
    "13:02:10"
  ]
}
```

---

## Botão COMIDA — GPIO 14

Exibe:

```json
{
  "visitasComida": 5,
  "visitaHorario": [
    "08:10:22",
    "12:40:11"
  ]
}
```

---

# 📡 Conectividade

O sistema:
- conecta automaticamente ao Wi-Fi
- sincroniza horário via NTP
- cria um servidor HTTP local
- disponibiliza os dados em JSON

---

# 🧠 Lógica de Detecção

Os sensores ultrassônicos medem distância continuamente.

O sistema considera presença quando a distância medida for menor que:

```cpp
const int LIMITE = 15;
```

Isso significa:
- pet próximo do recipiente
- evento registrado
- contador incrementado

---

# 🧪 Simulação no Wokwi

🔗 https://wokwi.com/projects/463362553076345857

---

# 💻 Repositório GitHub

🔗 https://github.com/ZeDio/Challenger_IOT

---

# 🚀 Possíveis Evoluções

O projeto pode evoluir para:

- dashboard web
- aplicativo mobile
- histórico completo do pet
- análise comportamental
- inteligência artificial
- alertas automáticos
- acompanhamento remoto
- integração veterinária

---

# 👨‍💻 Equipe

Projeto desenvolvido por:

- ZeDio
- Arth.pv
- Marixavq
- JuliaTButtler
- Taikawaititi

---

# 📚 Projeto Acadêmico

Projeto desenvolvido para a disciplina:

**Disruptive Architectures: IoT, IoB & Generative AI**

---

# 📚 Projeto Acadêmico

Projeto desenvolvido para a disciplina:

**Disruptive Architectures: IoT, IoB & Generative AI**
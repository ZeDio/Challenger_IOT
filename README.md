# 🐾 Challenger IoT — CLYVO VET

Sistema IoT para monitoramento inteligente do comportamento alimentar e de hidratação de pets utilizando ESP32, sensores ultrassônicos e dashboard via API JSON.

---

# 📖 Sobre o Projeto

O **CLYVO VET** surgiu com o objetivo de auxiliar tutores e veterinários no acompanhamento contínuo da saúde animal.

A proposta do projeto é transformar ações simples do dia a dia — como comer e beber água — em dados úteis para acompanhamento clínico e análise comportamental.

O sistema utiliza:

- ESP32
- Sensores ultrassônicos HC-SR04
- Display LCD I2C
- Wi-Fi
- API REST em JSON

---

# 🎯 Problema

Grande parte dos tutores:

- não possui histórico estruturado do pet
- não acompanha mudanças comportamentais
- só percebe problemas em situações críticas

Isso dificulta:
- diagnósticos veterinários
- prevenção de doenças
- identificação de alterações de comportamento

---

# 💡 Solução

O sistema monitora automaticamente:

✅ frequência de alimentação  
✅ frequência de hidratação  
✅ horário das visitas aos recipientes  

Esses dados podem ser utilizados futuramente em:
- dashboards
- aplicativos
- sistemas veterinários
- análise comportamental
- inteligência artificial

---

# 🧠 Funcionamento

Os sensores HC-SR04 identificam quando o pet se aproxima:
- do recipiente de comida
- do recipiente de água

Quando isso acontece:
1. o sistema registra a visita
2. salva o horário via NTP
3. atualiza os contadores
4. exibe informações no LCD
5. disponibiliza os dados via API JSON

---

# 🖥️ Preview do Projeto

![Projeto IoT](./Projeto_IOT.png)

---

# 🔧 Tecnologias Utilizadas

## Hardware
- ESP32
- HC-SR04
- LCD I2C 16x2
- Protoboard

---

## Software
- Arduino C++
- Wokwi
- WiFi.h
- WebServer.h
- LiquidCrystal_I2C
- NTP

---

# 🌐 API REST

O ESP32 cria um pequeno servidor HTTP.

---

## `/status`

Retorna o resumo geral:

```json
{
  "visitasComida": 5,
  "visitasAgua": 3
}
```

---

## `/comida`

Retorna:
- quantidade de visitas
- horários registrados

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

## `/agua`

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

# 📡 Conectividade

O sistema:
- conecta no Wi-Fi
- sincroniza horário automaticamente via NTP
- exibe IP no LCD
- disponibiliza API local

---

# 🧠 Interface LCD

Durante o funcionamento:

## Inicialização
```text
Iniciando...
```

---

## Wi-Fi
```text
WiFi conectado
```

---

## IP
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

# 🐶 Aplicações Futuras

O projeto pode evoluir para:

- integração com veterinários
- dashboards web
- histórico completo do pet
- análise de comportamento
- IA para prevenção
- alertas automáticos
- acompanhamento remoto

---

# 🚀 Simulação no Wokwi

🔗 https://wokwi.com/projects/463362553076345857

---

# 💻 Repositório GitHub

🔗 https://github.com/ZeDio/Challenger_IOT

---

# ⚙️ Como Funciona

## 1. Sensores

Os sensores ultrassônicos medem distância continuamente.

Quando o pet aproxima:
- a distância diminui
- o sistema identifica presença

---

## 2. Detecção

Se a distância estiver abaixo do limite definido:

```cpp
const int LIMITE = 15;
```

o sistema considera:
```text
"pet próximo do recipiente"
```

---

## 3. Registro

O ESP32:
- incrementa o contador
- pega horário via internet (NTP)
- salva o evento

---

## 4. Exibição

O LCD:
- mostra eventos em tempo real
- atualiza alimentação e hidratação

---

## 5. API

Todos os dados ficam disponíveis via JSON para integração com:
- dashboards
- aplicativos
- sistemas externos

---

# 👨‍💻 Autor

Projeto desenvolvido por:

**ZeDio - Arth.pv - Marixavq - JuliaTButtler - Taikawaititi**

---

# 📚 Projeto Acadêmico

Projeto desenvolvido para a disciplina:

**Disruptive Architectures: IoT, IoB & Generative AI**
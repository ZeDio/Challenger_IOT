// =========================
// Challenger IOT - CLYVO VET
// =========================

// =========================
// Libraries
// =========================
#include <WiFi.h>
#include <WebServer.h>
#include <time.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// =========================
// LCD I2C
// =========================
LiquidCrystal_I2C lcd(0x27, 16, 2);

// =========================
// WIFI
// =========================
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// =========================
// NTP
// =========================
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 3600;
const int daylightOffset_sec = 0;

// =========================
// SERVIDOR
// =========================
WebServer server(80);

// =========================
// PINOS SENSOR COMIDA
// =========================
#define TRIG_COMIDA 5
#define ECHO_COMIDA 18

// =========================
// PINOS SENSOR AGUA
// =========================
#define TRIG_AGUA 15
#define ECHO_AGUA 2

// =========================
// BOTÕES
// =========================
#define BTN_STATUS 13
#define BTN_AGUA 12
#define BTN_COMIDA 14

// =========================
// CONTADORES
// =========================
int visitasComida = 0;
int visitasAgua = 0;

// =========================
// CONTROLE
// =========================
bool detectouComida = false;
bool detectouAgua = false;

// =========================
// ESTADO BOTÕES
// =========================
bool ultimoEstadoStatus = HIGH;
bool ultimoEstadoAgua = HIGH;
bool ultimoEstadoComida = HIGH;

// =========================
// HORÁRIOS
// =========================
String horariosComida[50];
String horariosAgua[50];

// =========================
// HISTÓRICO DIÁRIO
// =========================
String datas[30];

int historicoComida[30];
int historicoAgua[30];

int totalDias = 0;

String dataAtual = "";

// =========================
// LIMITE
// =========================
const int LIMITE = 15;

// =========================
// ATUALIZAR LCD
// =========================
void atualizarLCD() {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Refeicoes: ");
  lcd.print(visitasComida);

  lcd.setCursor(0, 1);
  lcd.print("Hidratacao: ");
  lcd.print(visitasAgua);
}

// =========================
// MOSTRAR EVENTO LCD
// =========================
void mostrarEventoLCD(String mensagem, String horario) {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(mensagem);

  lcd.setCursor(0, 1);
  lcd.print(horario);

  delay(3000);

  atualizarLCD();
}

// =========================
// PEGAR HORÁRIO
// =========================
String pegarHorario() {

  struct tm timeinfo;

  if (!getLocalTime(&timeinfo)) {
    return "Horario indisponivel";
  }

  char horario[10];

  strftime(horario, sizeof(horario), "%H:%M:%S", &timeinfo);

  return String(horario);
}

// =========================
// PEGAR DATA
// =========================
String pegarData() {

  struct tm timeinfo;

  if (!getLocalTime(&timeinfo)) {
    return "00/00/0000";
  }

  char data[11];

  strftime(data, sizeof(data), "%d/%m/%Y", &timeinfo);

  return String(data);
}

// =========================
// VERIFICAR NOVO DIA
// =========================
void verificarNovoDia() {

  String hoje = pegarData();

  // Primeiro dia
  if (dataAtual == "") {

    dataAtual = hoje;

    datas[totalDias] = hoje;
    historicoComida[totalDias] = 0;
    historicoAgua[totalDias] = 0;

    totalDias++;
  }

  // Virou o dia
  if (hoje != dataAtual) {

    dataAtual = hoje;

    visitasComida = 0;
    visitasAgua = 0;

    // Limpa horários
    for (int i = 0; i < 50; i++) {

      horariosComida[i] = "";
      horariosAgua[i] = "";
    }

    datas[totalDias] = hoje;

    historicoComida[totalDias] = 0;
    historicoAgua[totalDias] = 0;

    totalDias++;

    Serial.println("");
    Serial.println("===== NOVO DIA =====");
    Serial.println(hoje);

    atualizarLCD();
  }
}

// =========================
// JSON STATUS
// =========================
String gerarJsonStatus() {

  String json = "{";

  json += "\"data\":\"";
  json += dataAtual;
  json += "\",";

  json += "\"visitasComida\":";
  json += visitasComida;
  json += ",";

  json += "\"visitasAgua\":";
  json += visitasAgua;

  json += "}";

  return json;
}

// =========================
// JSON COMIDA
// =========================
String gerarJsonComida() {

  String json = "{";

  json += "\"data\":\"";
  json += dataAtual;
  json += "\",";

  json += "\"visitasComida\":";
  json += visitasComida;
  json += ",";

  json += "\"visitaHorario\":[";

  for (int i = 0; i < visitasComida; i++) {

    json += "\"";
    json += horariosComida[i];
    json += "\"";

    if (i < visitasComida - 1) {
      json += ",";
    }
  }

  json += "]}";

  return json;
}

// =========================
// JSON AGUA
// =========================
String gerarJsonAgua() {

  String json = "{";

  json += "\"data\":\"";
  json += dataAtual;
  json += "\",";

  json += "\"visitasAgua\":";
  json += visitasAgua;
  json += ",";

  json += "\"visitaHorario\":[";

  for (int i = 0; i < visitasAgua; i++) {

    json += "\"";
    json += horariosAgua[i];
    json += "\"";

    if (i < visitasAgua - 1) {
      json += ",";
    }
  }

  json += "]}";

  return json;
}

// =========================
// JSON HISTÓRICO
// =========================
String gerarJsonHistorico() {

  String json = "{";

  for (int i = 0; i < totalDias; i++) {

    json += "\"";
    json += datas[i];
    json += "\":{";

    json += "\"visitasComida\":";
    json += historicoComida[i];
    json += ",";

    json += "\"visitasAgua\":";
    json += historicoAgua[i];

    json += "}";

    if (i < totalDias - 1) {
      json += ",";
    }
  }

  json += "}";

  return json;
}

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(115200);

  // =========================
  // LCD
  // =========================
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  delay(2000);

  // =========================
  // Sensores
  // =========================
  pinMode(TRIG_COMIDA, OUTPUT);
  pinMode(ECHO_COMIDA, INPUT);

  pinMode(TRIG_AGUA, OUTPUT);
  pinMode(ECHO_AGUA, INPUT);

  // =========================
  // BOTÕES
  // =========================
  pinMode(BTN_STATUS, INPUT_PULLUP);
  pinMode(BTN_AGUA, INPUT_PULLUP);
  pinMode(BTN_COMIDA, INPUT_PULLUP);

  // =========================
  // WIFI
  // =========================
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Conectando");

  lcd.setCursor(0, 1);
  lcd.print("WiFi...");

  Serial.println("Conectando WiFi...");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado!");

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("WiFi conectado");

  delay(2000);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("IP:");

  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());

  delay(4000);

  // =========================
  // NTP
  // =========================
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  verificarNovoDia();

  // =========================
  // STATUS
  // =========================
  server.on("/status", []() {

    String json = gerarJsonStatus();

    Serial.println("");
    Serial.println("===== /status =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // COMIDA
  // =========================
  server.on("/comida", []() {

    String json = gerarJsonComida();

    Serial.println("");
    Serial.println("===== /comida =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // AGUA
  // =========================
  server.on("/agua", []() {

    String json = gerarJsonAgua();

    Serial.println("");
    Serial.println("===== /agua =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // HISTÓRICO
  // =========================
  server.on("/historico", []() {

    String json = gerarJsonHistorico();

    Serial.println("");
    Serial.println("===== /historico =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // DASHBOARD HTML
  // =========================
  server.on("/", []() {

    String html = R"rawliteral(

  <!DOCTYPE html>
  <html lang="pt-br">
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CLYVO VET - Challenger</title>

  <style>

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
  }

  body {
    background: #131313;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }

  .container {
    width: 100%;
    max-width: 900px;
  }

  .title {
    text-align: center;
    margin-bottom: 30px;
  }

  .title h1 {
    font-size: 38px;
    margin-bottom: 10px;
  }

  .title p {
    color: #FFFFFF;
  }

  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }

  .card {
    background: #161616;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
  }

  .card h2 {
    font-size: 20px;
    margin-bottom: 15px;
  }

  .value {
    font-size: 50px;
    font-weight: bold;
  }


  </style>
  </head>
  <body>

  <div class="container">

    <div class="title">
      <h1>CLYVO VET Challenger</h1>
      <p>Monitoramento Inteligente de Pets</p>
    </div>

    <div class="cards">

      <div class="card">
        <h2>🍖 Refeições</h2>
        <div class="value" id="comida">0</div>
      </div>

      <div class="card">
        <h2>💧 Hidratações</h2>
        <div class="value" id="agua">0</div>
      </div>

    </div>

  </div>

  <script>

  async function atualizarDados() {

    try {

      const response = await fetch('/status');
      const data = await response.json();

      document.getElementById('comida').innerText = data.visitasComida;
      document.getElementById('agua').innerText = data.visitasAgua;

    } catch (error) {

      console.log('Erro ao atualizar dados');
    }
  }

  atualizarDados();

  setInterval(atualizarDados, 2000);

  </script>

  </body>
  </html>

  )rawliteral";

    server.send(200, "text/html", html);
  });

  // =========================
  // START SERVER
  // =========================
  server.begin();

  Serial.println("");
  Serial.println("Servidor iniciado!");
  Serial.println(WiFi.localIP());

  atualizarLCD();
}

// =========================
// LOOP
// =========================
void loop() {

  server.handleClient();

  verificarNovoDia();

  // =========================
  // BOTÃO STATUS
  // =========================
  bool estadoStatus = digitalRead(BTN_STATUS);

  if (ultimoEstadoStatus == HIGH && estadoStatus == LOW) {

    Serial.println("");
    Serial.println("===== /status =====");
    Serial.println(gerarJsonStatus());
  }

  ultimoEstadoStatus = estadoStatus;

  // =========================
  // BOTÃO AGUA
  // =========================
  bool estadoAgua = digitalRead(BTN_AGUA);

  if (ultimoEstadoAgua == HIGH && estadoAgua == LOW) {

    Serial.println("");
    Serial.println("===== /agua =====");
    Serial.println(gerarJsonAgua());
  }

  ultimoEstadoAgua = estadoAgua;

  // =========================
  // BOTÃO COMIDA
  // =========================
  bool estadoComida = digitalRead(BTN_COMIDA);

  if (ultimoEstadoComida == HIGH && estadoComida == LOW) {

    Serial.println("");
    Serial.println("===== /comida =====");
    Serial.println(gerarJsonComida());
  }

  ultimoEstadoComida = estadoComida;

  // =========================
  // SENSOR COMIDA
  // =========================
  float distanciaComida = medirDistancia(TRIG_COMIDA, ECHO_COMIDA);

  if (distanciaComida > 0 && distanciaComida <= LIMITE) {

    if (!detectouComida) {

      detectouComida = true;

      String horario = pegarHorario();

      horariosComida[visitasComida] = horario;

      visitasComida++;

      historicoComida[totalDias - 1] = visitasComida;

      Serial.println("");
      Serial.println("Pet foi comer!");

      mostrarEventoLCD("Pet comeu!", horario);
    }

  } else {

    detectouComida = false;
  }

  // =========================
  // SENSOR AGUA
  // =========================
  float distanciaAgua = medirDistancia(TRIG_AGUA, ECHO_AGUA);

  if (distanciaAgua > 0 && distanciaAgua <= LIMITE) {

    if (!detectouAgua) {

      detectouAgua = true;

      String horario = pegarHorario();

      horariosAgua[visitasAgua] = horario;

      visitasAgua++;

      historicoAgua[totalDias - 1] = visitasAgua;

      Serial.println("");
      Serial.println("Pet foi beber agua!");

      mostrarEventoLCD("Bebeu agua!", horario);
    }

  } else {

    detectouAgua = false;
  }

  delay(100);
}

// =========================
// MEDIR DISTÂNCIA
// =========================
float medirDistancia(int trigPin, int echoPin) {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  long duracao = pulseIn(echoPin, HIGH);

  float distancia = duracao * 0.034 / 2;

  return distancia;
}
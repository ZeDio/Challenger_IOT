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
// JSON STATUS
// =========================
String gerarJsonStatus() {

  String json = "{";

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

  // =========================
  // STATUS
  // =========================
  server.on("/status", []() {

    String json = gerarJsonStatus();

    Serial.println("===== /status =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // COMIDA
  // =========================
  server.on("/comida", []() {

    String json = gerarJsonComida();

    Serial.println("===== /comida =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // AGUA
  // =========================
  server.on("/agua", []() {

    String json = gerarJsonAgua();

    Serial.println("===== /agua =====");
    Serial.println(json);

    server.send(200, "application/json", json);
  });

  // =========================
  // START SERVER
  // =========================
  server.begin();

  Serial.println("Servidor iniciado!");
  Serial.println(WiFi.localIP());

  atualizarLCD();
}

// =========================
// LOOP
// =========================
void loop() {

  server.handleClient();

  // =========================
  // LEITURA BOTÃO STATUS
  // =========================
  bool estadoStatus = digitalRead(BTN_STATUS);

  if (ultimoEstadoStatus == HIGH && estadoStatus == LOW) {

    Serial.println("");
    Serial.println("===== /status =====");
    Serial.println(gerarJsonStatus());
  }

  ultimoEstadoStatus = estadoStatus;

  // =========================
  // LEITURA BOTÃO AGUA
  // =========================
  bool estadoAgua = digitalRead(BTN_AGUA);

  if (ultimoEstadoAgua == HIGH && estadoAgua == LOW) {

    Serial.println("");
    Serial.println("===== /agua =====");
    Serial.println(gerarJsonAgua());
  }

  ultimoEstadoAgua = estadoAgua;

  // =========================
  // LEITURA BOTÃO COMIDA
  // =========================
  bool estadoComida = digitalRead(BTN_COMIDA);

  if (ultimoEstadoComida == HIGH && estadoComida == LOW) {

    Serial.println("");
    Serial.println("===== /comida =====");
    Serial.println(gerarJsonComida());
  }

  ultimoEstadoComida = estadoComida;

  // =========================
  // COMIDA
  // =========================
  float distanciaComida = medirDistancia(TRIG_COMIDA, ECHO_COMIDA);

  if (distanciaComida > 0 && distanciaComida <= LIMITE) {

    if (!detectouComida) {

      detectouComida = true;

      String horario = pegarHorario();

      horariosComida[visitasComida] = horario;

      visitasComida++;

      Serial.println("");
      Serial.println("Pet foi comer!");

      mostrarEventoLCD("Pet comeu!", horario);
    }

  } else {

    detectouComida = false;
  }

  // =========================
  // AGUA
  // =========================
  float distanciaAgua = medirDistancia(TRIG_AGUA, ECHO_AGUA);

  if (distanciaAgua > 0 && distanciaAgua <= LIMITE) {

    if (!detectouAgua) {

      detectouAgua = true;

      String horario = pegarHorario();

      horariosAgua[visitasAgua] = horario;

      visitasAgua++;

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
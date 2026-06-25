#include <Servo.h>

Servo servo;

const int trigPin = 10;
const int echoPin = 11;
const int servoPin = 9;
const int buzzerPin = 6;

const int UMBRAL_ACTIVACION = 5;
const int UMBRAL_DESACTIVACION = 8;

int angle = 0;
int direction = 1;

bool alertaActiva = false;
bool melodiaTocada = false;

// ===============================
// SUPER MARIO BROS - Versión larga
// ===============================

const int melodia[][2] = {

  {659,150}, {659,150}, {0,150}, {659,150},
  {0,150}, {523,150}, {659,150},
  {784,300}, {0,300}, {392,300}

};

const int NOTAS = sizeof(melodia) / sizeof(melodia[0]);

// ===============================
// TOCAR MELODÍA
// ===============================

void tocarMelodia() {

  for (int i = 0; i < NOTAS; i++) {

    if (melodia[i][0] == 0) {
      noTone(buzzerPin);
    } else {
      tone(buzzerPin, melodia[i][0]);
    }

    delay(melodia[i][1]);

    noTone(buzzerPin);

    delay(30);
  }
}

// ===============================
// SENSOR ULTRASÓNICO
// ===============================

long medirDistancia() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  long duracion = pulseIn(echoPin, HIGH, 30000);

  long distancia = duracion * 0.034 / 2;

  if (distancia == 0 || distancia > 200) {
    distancia = 200;
  }

  return distancia;
}

// ===============================
// SETUP
// ===============================

void setup() {

  Serial.begin(9600);

  servo.attach(servoPin);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
}

// ===============================
// LOOP PRINCIPAL
// ===============================

void loop() {

  servo.write(angle);

  delay(30);

  long dist = medirDistancia();

  Serial.print(angle);
  Serial.print(",");
  Serial.println(dist);

  // Histéresis

  if (!alertaActiva && dist < UMBRAL_ACTIVACION) {

    alertaActiva = true;
    melodiaTocada = false;

  } else if (alertaActiva && dist > UMBRAL_DESACTIVACION) {

    alertaActiva = false;
    melodiaTocada = false;
  }

  // Tocar melodía una vez

  if (alertaActiva && !melodiaTocada) {

    tocarMelodia();

    melodiaTocada = true;
  }

  // Movimiento del radar

  angle += direction;

  if (angle >= 180) {
    direction = -1;
  }

  if (angle <= 0) {
    direction = 1;
  }
}

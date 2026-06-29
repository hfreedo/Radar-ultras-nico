#include <Servo.h>

Servo servo;

const int trigPin = 10;
const int echoPin = 11;
const int servoPin = 9;
const int buzzerPin = 6;

int UMBRAL_ACTIVACION = 5;
int UMBRAL_DESACTIVACION = 8;

int angle = 0;
int direction = 1;

int moveDelay = 30;
bool alertaActiva = false;
bool melodiaTocada = false;
bool mute = false;
bool paused = false;

unsigned long lastMove = 0;

const int melodia[][2] = {
  {1047, 60}, {0, 20},
  {1319, 60}, {0, 20},
  {1568, 60}, {0, 20},
  {2093, 150}
};

const int NOTAS = sizeof(melodia) / sizeof(melodia[0]);

void tocarMelodia() {
  if (mute) return;
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

long medirDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duracion = pulseIn(echoPin, HIGH, 30000);
  long distancia = duracion * 0.034 / 2;

  if (distancia == 0 || distancia > 400) {
    distancia = 400;
  }
  return distancia;
}

void handleCommand(String cmd) {
  if (cmd.startsWith("VEL:")) {
    int val = cmd.substring(4).toInt();
    if (val >= 5 && val <= 200) {
      moveDelay = val;
      Serial.print("OK VEL:"); Serial.println(moveDelay);
    }
  } else if (cmd.startsWith("THR:")) {
    int val = cmd.substring(4).toInt();
    if (val >= 2 && val <= 100) {
      UMBRAL_ACTIVACION = val;
      UMBRAL_DESACTIVACION = val + 3;
      Serial.print("OK THR:"); Serial.println(val);
    }
  } else if (cmd.startsWith("MUTE:")) {
    mute = cmd.substring(5).toInt() == 1;
    Serial.print("OK MUTE:"); Serial.println(mute ? 1 : 0);
    if (!mute) noTone(buzzerPin);
  } else if (cmd.startsWith("PAUSE:")) {
    paused = cmd.substring(6).toInt() == 1;
    Serial.print("OK PAUSE:"); Serial.println(paused ? 1 : 0);
  }
}

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);

  Serial.println("RADAR_READY");
}

void loop() {
  while (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() > 0) handleCommand(cmd);
  }

  if (paused) {
    delay(50);
    return;
  }

  if (millis() - lastMove >= (unsigned long)moveDelay) {
    lastMove = millis();

    servo.write(angle);
    delay(15);

    long dist = medirDistancia();
    int displayAngle = 180 - angle;

    Serial.print(displayAngle);
    Serial.print(",");
    Serial.println(dist);

    if (!alertaActiva && dist < UMBRAL_ACTIVACION) {
      alertaActiva = true;
      melodiaTocada = false;
    } else if (alertaActiva && dist > UMBRAL_DESACTIVACION) {
      alertaActiva = false;
      melodiaTocada = false;
    }

    if (alertaActiva && !melodiaTocada) {
      tocarMelodia();
      melodiaTocada = true;
    }

    angle += direction;
    if (angle >= 180) direction = -1;
    if (angle <= 0) direction = 1;
  }
}

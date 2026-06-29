# Conexión Del Hardware

Pines usados por el firmware principal:

```text
HC-SR04 TRIG  -> pin 10
HC-SR04 ECHO  -> pin 11
Servo señal   -> pin 9
Buzzer        -> pin 6
Baudrate      -> 9600
```

Notas:

- Alimentar el servo de forma estable. Si se mueve errático, usar fuente externa de 5 V y compartir GND con Arduino.
- El sensor ultrasónico funciona mejor cuando apunta a superficies planas.
- Si el buzzer se activa demasiado, subir el umbral de alerta desde la interfaz.

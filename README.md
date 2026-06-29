# Radar Ultrasónico Web

[![Plataforma](https://img.shields.io/badge/plataforma-Windows-2563eb)](https://github.com/hfreedo/Radar-ultrasonico-arduino)
[![Arduino](https://img.shields.io/badge/hardware-Arduino%20UNO-00979d)](https://github.com/hfreedo/Radar-ultrasonico-arduino)
[![Release](https://img.shields.io/github/v/release/hfreedo/Radar-ultrasonico-arduino?label=versi%C3%B3n&color=51e898)](https://github.com/hfreedo/Radar-ultrasonico-arduino/releases)

Interfaz web portable para un radar ultrasónico con Arduino, sensor HC-SR04, servomotor y buzzer.
La aplicación lee datos por puerto serie, dibuja el barrido del radar en el navegador y permite controlar velocidad, umbral de alerta, pausa y silencio del buzzer.

![Radar ultrasónico web](docs/radar-preview.png)

## Descarga portable

La opción recomendada para otra PC es descargar [`RadarWebPortable.zip`](https://github.com/hfreedo/Radar-ultrasonico-arduino/releases/latest/download/RadarWebPortable.zip).

Después de descomprimirlo, ejecutar:

```
RadarUltrasonicoWeb.exe
```

No requiere instalar Python. Solo necesita Windows, un navegador moderno y el driver USB de la placa Arduino.

La aplicación abre automáticamente `http://127.0.0.1:8765`.

## Funciones

- Barrido de radar animado en tiempo real con efecto de estela.
- Detección visual de objetos con indicador de ángulo y distancia.
- Control de velocidad de barrido (5 a 200 ms por paso).
- Umbral de alerta configurable (2 a 100 cm) con activación del buzzer.
- Silencio y pausa del barrido desde la interfaz.
- Selección y conexión del puerto COM.

## Hardware necesario

- Arduino UNO, Nano o compatible.
- Sensor ultrasónico HC-SR04.
- Servomotor.
- Buzzer.
- Cable USB de datos.
- Jumpers.

## Conexiones

| Componente     | Arduino UNO |
|----------------|-------------|
| HC-SR04 TRIG   | D10         |
| HC-SR04 ECHO   | D11         |
| Servo señal    | D9          |
| Buzzer         | D6          |

Comunicación serial a `9600` baudios.

## Preparar el Arduino

1. Abrir [`arduino/radar/Proyecto_RADAR_ultras_nico.ino`](arduino/radar/Proyecto_RADAR_ultras_nico.ino).
2. Seleccionar Arduino UNO y el puerto correspondiente.
3. Cargar el programa.
4. Cerrar el Monitor Serie antes de usar la aplicación.

El firmware barre de 0° a 180° con el servomotor, mide la distancia con el HC-SR04 y envía `angulo,distancia` por serial. Acepta comandos `VEL:<ms>`, `THR:<cm>`, `MUTE:<0|1>` y `PAUSE:<0|1>` desde la interfaz.

## Ejecutar desde el código fuente

```bat
python -m pip install -r requirements.txt
python server.py
```

O simplemente:

```bat
run.bat
```

La aplicación abre automáticamente `http://127.0.0.1:8765`.

## Generar nuevamente el paquete

En Windows, ejecutar:

```bat
tools\build_portable.bat
```

El proceso instala las herramientas de construcción, crea `dist/RadarUltrasonicoWeb.exe` y organiza el paquete portable.

## Estructura principal

```
arduino/radar/               Firmware del Arduino
static/                      Interfaz HTML del radar
docs/                        Capturas y documentación
tools/                       Scripts de construcción y GUI alternativa
server.py                    Servidor local y conexión serial
RadarWebPortable.zip         Paquete listo para usar
```

## Estructura del paquete portable

```
RadarWebPortable/
  LEEME_PRIMERO.md
  RadarUltrasonicoWeb.exe
  static/
    index.html
  firmware/
    Proyecto_RADAR_ultras_nico.ino
  docs/
    README_PORTABLE_WEB.md
    CONEXION_ARDUINO.md
    EMPAQUETADO.md
```

## Solución de problemas

### No aparece ningún puerto COM

- Revisá que el cable USB sea de datos.
- Probá otro puerto USB.
- Instalá el driver CH340/CH341 o CP210x según tu placa.
- Cerrá Arduino IDE u otros monitores serie antes de conectar.

### La app abre pero no recibe datos

- Verificá que el firmware correcto esté cargado.
- Confirmá que el baudrate sea `9600`.
- Presioná `CONECTAR` en la interfaz.
- Revisá que el Arduino no esté usando otro sketch.

### El navegador no abre

Entrá manualmente a `http://127.0.0.1:8765`.

### Windows muestra advertencia de seguridad

Es normal en ejecutables no firmados. Si el archivo viene del release oficial, se puede permitir la ejecución.

## Licencia

Este proyecto se distribuye bajo licencia MIT.

Puede utilizarse, modificarse y compartirse libremente con fines educativos, manteniendo el aviso de autoría y la licencia original. Ver [LICENSE](LICENSE).

# Radar Ultrasónico Web Portable

Este paquete usa la versión web del radar. El ejecutable levanta un servidor local y abre la interfaz en el navegador en:

```text
http://127.0.0.1:8765
```

## Requisitos en la PC destino

- Windows.
- Navegador web moderno.
- Driver USB de la placa Arduino o conversor USB-Serie.
- Arduino cargado con el firmware incluido en `firmware/Proyecto_RADAR_ultras_nico.ino`.

No hace falta instalar Python si se usa el ejecutable empaquetado.

## Uso rápido

1. Conectar el Arduino por USB.
2. Ejecutar `RadarUltrasonicoWeb.exe`.
3. Esperar que se abra el navegador.
4. En la interfaz, elegir el puerto COM.
5. Presionar `CONECTAR`.

## Firmware recomendado

Usar este sketch:

```text
firmware/Proyecto_RADAR_ultras_nico.ino
```

Ese firmware emite datos por serial a `9600` baudios con el formato:

```text
angulo,distancia
```

También acepta comandos desde la interfaz:

```text
VEL:<ms>
THR:<cm>
MUTE:<0|1>
PAUSE:<0|1>
```

## Si no aparece el puerto COM

- Verificar cable USB de datos, no solo carga.
- Revisar el Administrador de dispositivos de Windows.
- Instalar el driver correspondiente a la placa:
  - CH340/CH341 para muchas placas Arduino compatibles.
  - CP210x para algunas placas con conversor Silicon Labs.
  - Driver oficial si se usa Arduino original.

## Si el navegador no abre

Abrir manualmente:

```text
http://127.0.0.1:8765
```

## Archivos principales

```text
RadarUltrasonicoWeb.exe
static/index.html
firmware/Proyecto_RADAR_ultras_nico.ino
docs/README_PORTABLE_WEB.md
```

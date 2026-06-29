# Empaquetado

## Construir ejecutable web

Desde la raíz del proyecto:

```bat
tools\build_web_exe.bat
```

El ejecutable queda en:

```text
dist/RadarUltrasonicoWeb.exe
```

## Crear paquete exportable

El paquete recomendado debe contener:

```text
RadarWebPortable/
  RadarUltrasonicoWeb.exe
  static/
    index.html
  firmware/
    Proyecto_RADAR_ultras_nico.ino
  docs/
    README_PORTABLE_WEB.md
    CONEXION_ARDUINO.md
```

Si se usa `--onefile` con PyInstaller, el ejecutable ya trae `static/index.html` embebido. Aun así, se puede incluir la carpeta `static/` como respaldo y para facilitar edición visual futura.

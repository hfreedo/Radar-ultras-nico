@echo off
setlocal
cd /d "%~dp0.."

python -m pip install -r requirements-web.txt
python -m pip install pyinstaller

python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name RadarUltrasonicoWeb ^
  --add-data "Radar con Python\static;static" ^
  "Radar con Python\server.py"

echo.
echo Ejecutable generado en:
echo %cd%\dist\RadarUltrasonicoWeb.exe

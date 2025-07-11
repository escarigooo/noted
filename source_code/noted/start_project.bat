@echo off
cd /d "%~dp0"

REM Iniciar o WAMP
start "" "C:\wamp64\wampmanager.exe"
timeout /t 5 >nul

REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Configurar e correr o Flask
set FLASK_APP=app.py
set FLASK_DEBUG=True
flask run

pause

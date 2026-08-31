@echo off
REM Ativar ambiente virtual e instalar dependências

cd /d "%~dp0.."

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

echo Ambiente instalado com sucesso!
pause

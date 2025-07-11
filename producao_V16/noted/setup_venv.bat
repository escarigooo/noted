@echo off
REM Ativar ambiente virtual e instalar dependências

python -m venv venv
call venv\Scripts\activate

pip install --upgrade pip

pip install -r requirements.txt

pip install python-dotenv
pip install pandas matplotlib sqlalchemy mysql-connector-python
pip install papermill
pip install nbformat==5.9.2 nbconvert jupyter_client

pip install werkzeug

pip install jupyter nbconvert mysql-connector-python

pip install email_validator

echo Ambiente instalado com sucesso!
pause

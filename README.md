# Create ambiente virtual local

`python3 -m venv venv`

# Ativar ambiente virtual criado

`source venv/bin/activate`

# instalar certificado

`brew install openssl env PATH="/usr/local/opt/openssl/bin:$PATH" pyenv install 3.11.7`

# Desativar ambiente virtual criado

`deactivate`

# Config navegador to RUN

//Mac
/Applications/Chromium.app/Contents/MacOS/Chromium

# VARIAVEIS DE EXECUÇÃO DO PROJETO

START_COMMAND=python run.py

HUAWEI_HOST=191.7.2.217
HUAWEI_USERNAME='teste1'
HUAWEI_PASSWORD='Mudar@#1231'
HUAWEI_PORT=1221

DB_HOST=huawei_back-end_mysql
DB_NAME=ravenbd
DB_USER=ravenuser
DB_PASS=ravenpass

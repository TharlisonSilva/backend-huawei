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

`START_COMMAND=gunicorn wsgi:app --bind 0.0.0.0:$PORT`

`HUAWEI_HOST=xxxxx`
`HUAWEI_USERNAME='xxxxxx'`
`HUAWEI_PASSWORD='xxxxxxx`
`HUAWEI_PORT=xxxx`

`DB_HOST=xxxx`
`DB_NAME=xxxx`
`DB_USER=xxxx`
`DB_PASS=xxxx`

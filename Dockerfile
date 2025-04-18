# Imagem base do Python (versão à sua escolha)
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

ENV PYTHONPATH=/app

# Copia apenas o arquivo de dependências primeiro (melhora cache)
COPY requirements.txt /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta local para o contêiner
COPY . /app

# Define o comando padrão para rodar seu aplicativo
CMD [ "python", "run.py" ]

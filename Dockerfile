# Use uma imagem base com Python
FROM python:3.11

# Defina o diretório de trabalho dentro do container
WORKDIR /roadbox_api

# Copie o arquivo de requisitos
COPY requirements.txt /roadbox_api/requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o diretório de trabalho no container
COPY . /roadbox_api

# Comando para executar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

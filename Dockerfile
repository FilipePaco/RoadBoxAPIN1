# Usar imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos para o container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo o conteúdo do projeto para o diretório de trabalho no container
COPY . .

# Configurar variáveis de ambiente para o Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE roadbox_api.settings

# Expor a porta do Django
EXPOSE 8000

# Comando para iniciar o servidor Django
CMD ["gunicorn", "roadbox_api.wsgi:application", "--bind", "0.0.0.0:8000"]

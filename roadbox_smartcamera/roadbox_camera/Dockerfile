# Dockerfile

# Usando a imagem base do Python
FROM python:3.11-slim

RUN python -m venv /opt/venv

COPY . .
RUN /opt/venv/bin/pip install -r requirements.txt


# Expondo a porta da aplicação (se necessário)
# Para aplicações que usam a webcam, você pode precisar expor a porta do vídeo:
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["/opt/venv/bin/python", "camera.py"]

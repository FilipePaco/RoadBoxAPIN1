import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Autenticação no Google Drive
gauth = GoogleAuth()
gauth.LoadCredentialsFile('settings.yaml')

"""if gauth.credentials is None:
    # Primeira autenticação, requer navegação e login
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh do token expirado
    gauth.Refresh()
else:
    # Autentica usando o token salvo
    gauth.Authorize()

# Salva as credenciais para reutilização
gauth.SaveCredentialsFile("settings.yaml")"""

drive = GoogleDrive(gauth)

print("Conectado ao Google Drive com sucesso.")

# Função para upload para o Google Drive e retornar o link compartilhável
def upload_to_drive(file_path):
    file_drive = drive.CreateFile({'title': os.path.basename(file_path)})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    file_drive.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })
    return file_drive['alternateLink']

# Teste de upload
file_path = 'teste4.png'  # Substitua pelo caminho correto
file_link = upload_to_drive(file_path)
print("Imagem enviada com sucesso! Link compartilhável:", file_link)

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
project_dir = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(project_dir, 'testedeapi-441500-8bc465207819.json')

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

def upload_image_to_drive(image_path):
    """
    Faz o upload de uma imagem para o Google Drive e retorna o link de visualização.

    :param image_path: Caminho completo do arquivo de imagem.
    :return: URL de visualização do arquivo.
    """
    # Verifica se o caminho da imagem é válido
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {image_path}")

    # Define os metadados do arquivo
    file_metadata = {
        'name': os.path.basename(image_path),  # Nome do arquivo
        'mimeType': 'image/jpeg'               # Tipo MIME para imagem JPEG
    }
    media = MediaFileUpload(image_path, mimetype='image/jpeg')

    # Cria o arquivo no Google Drive
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink, permissions'
    ).execute()

    # Define as permissões para público
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive_service.permissions().create(
        fileId=file['id'],
        body=permission,
        fields='id'
    ).execute()

    print(f"Arquivo '{file_metadata['name']}' criado com sucesso. ID: {file['id']}")
    print(f"Link de visualização: {file['webViewLink']}")  # Retorna o link de visualização

    return file['webViewLink']

def test():
    link = upload_image_to_drive("teste3.png")
    print(link)
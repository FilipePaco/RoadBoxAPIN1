import os
from ultralytics import YOLO
import cv2 as cv
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from .models import EnvioDeSinistro

project_dir = os.path.dirname(os.path.abspath(__file__))


cred_path = os.path.join(project_dir, 'settings.yaml')
if os.path.exists(cred_path):    
    print(f"Modelo carregado com sucesso de: {cred_path}")
else:
    raise FileNotFoundError(f"Arquivo de modelo não encontrado em: {cred_path}")
gauth = GoogleAuth()
gauth.LoadCredentialsFile(cred_path)

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("settings.yaml")

drive = GoogleDrive(gauth)

def salvar_no_banco(dispositivo, drive_link, latitude, longitude):
    EnvioDeSinistro.objects.create(
        dispositivo=dispositivo,
        foto_sinistro=drive_link,
        data_hora=datetime.now(),
        latitude=latitude,
        longitude=longitude
    )

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

def analyze_frames(frames, model: YOLO, dispositivo, latitude, longitude):
    global cursor
    coordinates = f'{longitude};{latitude}'
    """Analisa os frames usando o modelo YOLO, faz upload dos detectados para o Google Drive e salva o link no banco de dados."""
    num_classes = len(model.model.names)
    cores_deteccao = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_classes)]
    lista_classes = list(model.model.names.values())
    detected_frames = []

    coord_folder = f'media/frames/{coordinates}'
    os.makedirs(coord_folder, exist_ok=True)

    for frame_path in frames:
        image = cv.imread(frame_path)
        if image is None:
            print(f"Erro ao carregar a imagem: {frame_path}")
            continue

        results = model.track(source=image, conf=0.6, save=False, iou=0.20, imgsz=640, classes=0, device='cpu')
        if len(results) != 0:
            for deteccao in results:
                caixas = deteccao.boxes
                for caixa in caixas:
                    id_classe = int(caixa.cls[0])
                    confianca = float(caixa.conf[0])
                    bb = caixa.xyxy[0]

                    cv.rectangle(
                        image,
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        cores_deteccao[id_classe],
                        3
                    )
                    fonte = cv.FONT_HERSHEY_COMPLEX
                    cv.putText(
                        image,
                        f"{lista_classes[id_classe]} {round(confianca, 3)}",
                        (int(bb[0]), int(bb[1]) - 10),
                        fonte,
                        1,
                        (255, 255, 255),
                        2
                    )

                    frame_name = os.path.basename(frame_path)
                    save_path = os.path.join(coord_folder, frame_name)
                    cv.imwrite(save_path, image)
                    # Upload para o Google Drive e obter o link
                    drive_link = upload_to_drive(save_path)

                    salvar_no_banco(dispositivo=dispositivo,drive_link= drive_link,latitude= latitude,longitude= longitude)

                    detected_frames.append(drive_link)
                    break  # Saia do loop após salvar e fazer upload de um acidente

    return detected_frames

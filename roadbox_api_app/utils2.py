import os
from ultralytics import YOLO
import cv2 as cv
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sqlite3  # Exemplo usando SQLite
from datetime import datetime

# Autenticação no Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Autentica localmente
drive = GoogleDrive(gauth)

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

# Conectar ao banco de dados
conn = sqlite3.connect('detected_frames.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS enviodesinistro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dispositivo VARCHAR(50),
        foto_sinistro VARCHAR,  -- Armazena o link da imagem
        data_hora TIMESTAMP,
        latitude DECIMAL(10, 6),
        longitude DECIMAL(10, 6)
    )
''')

def analyze_frames(frames, coordinates, model: YOLO, dispositivo, latitude, longitude):
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

                    # Obter a data e hora atual
                    data_hora = datetime.now()

                    # Inserir os dados no banco de dados
                    cursor.execute('''
                        INSERT INTO enviodesinistro (dispositivo, foto_sinistro, data_hora, latitude, longitude)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (dispositivo, drive_link, data_hora, latitude, longitude))
                    conn.commit()

                    detected_frames.append(drive_link)
                    break  # Saia do loop após salvar e fazer upload de um acidente

    return detected_frames

# Fecha a conexão com o banco após uso
conn.close()

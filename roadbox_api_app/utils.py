import os
import requests
from ultralytics import YOLO
import cv2 as cv
import random
from datetime import datetime
from .models import EnvioDeSinistro
from .uploadimage import upload_image_to_drive



def salvar_no_banco(dispositivo, drive_link, latitude, longitude):
    ab = EnvioDeSinistro.objects.create(
        dispositivo=dispositivo,
        foto_sinistro=drive_link,
        data_hora=datetime.now(),
        latitude=latitude,
        longitude=longitude
    )    
    enviar_cloud_api(ab.id_envio)

    

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
                    # Configuração do texto
                    fonte = cv.FONT_HERSHEY_COMPLEX
                    tamanho_fonte = 0.8
                    cor_texto = (255, 255, 255)  # Branco
                    cor_contorno = (0, 0, 0)  # Preto

                    # Posição do texto (ajustada para não ser cortada)
                    x_text = max(int(bb[0]), 0)
                    y_text = max(int(bb[1]) - 10, 20)
                    texto = f"{lista_classes[id_classe]} {round(confianca, 3)}"
                     # Desenhar o texto com contorno
                    cv.putText(
                        image,
                        texto,
                        (x_text, y_text),
                        fonte,
                        tamanho_fonte,
                        cor_contorno,  # Contorno
                        thickness=4,
                        lineType=cv.LINE_AA
                    )
                    cv.putText(
                        image,
                        texto,
                        (x_text, y_text),
                        fonte,
                        tamanho_fonte,
                        cor_texto,  # Texto principal
                        thickness=2,
                        lineType=cv.LINE_AA
                    )

                    frame_name = os.path.basename(frame_path)
                    save_path = os.path.join(coord_folder, frame_name)
                    cv.imwrite(save_path, image)
                    # Upload para o Google Drive e obter o link
                    drive_link = upload_image_to_drive(save_path)

                    salvar_no_banco(dispositivo=dispositivo,drive_link= drive_link,latitude= latitude,longitude= longitude).id_envio
                    detected_frames.append(drive_link)
                    break  # Saia do loop após salvar e fazer upload de um acidente
    
    return detected_frames

def enviar_cloud_api(id_envio):
    # Exemplo de URL da API onde você deseja enviar o id_envio
    url_api = "https://roadboxcloudapi-production.up.railway.app/api/processar/"
    
    # Dados a serem enviados para a API
    dados = {
        "id_envio": id_envio
    }

    # Faz a requisição POST para a API
    response = requests.post(url_api, json=dados)

    if response.status_code == 200:
        print(f"ID envio {id_envio} enviado com sucesso para a API.")
    else:
        print(f"Erro ao enviar o ID envio {id_envio} para a API: {response.status_code}, {response.text}")

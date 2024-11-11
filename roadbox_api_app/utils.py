import os
from ultralytics import YOLO
import cv2 as cv
import random


def analyze_frames(frames, coordinates, model: YOLO):
    """Analisa os frames usando o modelo YOLO e salva aqueles que contêm acidentes."""
    # Obtendo o número máximo de classes detectadas pelo modelo
    num_classes = len(model.model.names)
    cores_deteccao = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_classes)]
    # Obtendo o nome de todas as classes do modelo
    lista_classes = list(model.model.names.values())
    
    detected_frames = []
    
    # Cria o diretório para as coordenadas se não existir
    coord_folder = f'media/frames/{coordinates}'
    os.makedirs(coord_folder, exist_ok=True)

    for frame_path in frames:
        # Carregar a imagem com OpenCV
        image = cv.imread(frame_path)
        if image is None:
            print(f"Erro ao carregar a imagem: {frame_path}")
            continue

        results = model.track(source=image, conf=0.6, save=False, iou=0.20, imgsz=640, classes=0, device='cpu')
        if len(results) != 0:
            for deteccao in results:
                caixas = deteccao.boxes
                for caixa in caixas:
                    print(f'Caixa detectada: {caixa}')
                    id_classe = int(caixa.cls[0])
                    confianca = float(caixa.conf[0])
                    bb = caixa.xyxy[0]

                    # Desenhando uma caixa delimitadora ao redor do objeto detectado
                    cv.rectangle(
                        image,
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        cores_deteccao[id_classe],
                        3
                    )

                    # Exibindo o nome da classe e a confiança da detecção
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
                    print('chegou aqui')

                    # Salvar o frame com a caixa desenhada na pasta das coordenadas
                    frame_name = os.path.basename(frame_path)
                    save_path = os.path.join(coord_folder, frame_name)
                    cv.imwrite(save_path, image)
                    
                    detected_frames.append(save_path)
                    break  # Saia do loop após salvar, já que um acidente foi detectado
    
    return detected_frames

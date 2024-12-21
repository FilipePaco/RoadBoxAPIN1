import cv2 as cv
import os
import random
import requests
from ultralytics import YOLO
from uploadimage import upload_image_to_drive

# Obtenha o caminho absoluto para o diretório atual do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Construa o caminho completo para o arquivo do modelo
model_path = os.path.join(project_dir, 'Detect-Accident.pt')

# Verifique se o arquivo existe antes de carregá-lo
if os.path.exists(model_path):
    model = YOLO(model_path)
    print(f"Modelo carregado com sucesso de: {model_path}")
else:
    raise FileNotFoundError(f"Arquivo de modelo não encontrado em: {model_path}")


def process_camera_feed(model: YOLO):
    latitude = '-16.876001'
    longitude = '-56.142302'
    dispositivo ='camera_01'
    
    coordinates = f'{longitude};{latitude}'
    coord_folder = f'media/frames/{coordinates}'
    os.makedirs(coord_folder, exist_ok=True)
    
    cap = cv.VideoCapture(0)  # Captura da câmera padrão
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    num_classes = len(model.model.names)
    cores_deteccao = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_classes)]
    lista_classes = list(model.model.names.values())

    detected_frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame.")
            break

        frame_count += 1
        results = model.track(source=frame, conf=0.6, save=False, iou=0.20, imgsz=640, classes=0, device='cpu')

        if results:
            for deteccao in results:
                caixas = deteccao.boxes
                for caixa in caixas:
                    id_classe = int(caixa.cls[0])
                    confianca = float(caixa.conf[0])
                    bb = caixa.xyxy[0]

                    # Desenho das caixas de detecção no frame
                    cv.rectangle(
                        frame,
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        cores_deteccao[id_classe],
                        3
                    )

                    fonte = cv.FONT_HERSHEY_COMPLEX
                    tamanho_fonte = 0.8
                    cor_texto = (255, 255, 255)
                    x_text = max(int(bb[0]), 0)
                    y_text = max(int(bb[1]) - 10, 20)
                    texto = f"{lista_classes[id_classe]} {round(confianca, 3)}"
                    cv.putText(
                        frame,
                        texto,
                        (x_text, y_text),
                        fonte,
                        tamanho_fonte,
                        cor_texto,
                        thickness=2,
                        lineType=cv.LINE_AA
                    )

                    frame_name = f"frame_{frame_count}.jpg"
                    save_path = os.path.join(coord_folder, frame_name)
                    cv.imwrite(save_path, frame)

                    # Upload para o Google Drive e obtenção do link
                    drive_link = upload_image_to_drive(save_path)

                    #fazer post no banco

                    detected_frames.append(drive_link)

                    # Salva os 5 principais frames e para
                    if len(detected_frames) >= 3:
                         # POST para o servidor
                        url = "http://127.0.0.1:8000/api/upload-camera/"  # Substitua pelo seu endpoint
                        payload = {
                            "latitude": latitude,
                            "longitude": longitude,
                            "links_frames": detected_frames[1],
                            "dispositivo": dispositivo
                        }
                        headers = {
                            "Content-Type": "application/json"
                        }

                        try:
                            response = requests.post(url, json=payload, headers=headers)
                            print("Resposta do servidor:", response.status_code, response.text)
                        except Exception as e:
                            print("Erro ao enviar os dados para o servidor:", e)
                        cap.release()
                        return detected_frames

        # Mostra o frame ao vivo para visualização
        cv.imshow("Detecção de Acidentes", frame)

        # Encerra com a tecla 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
    return detected_frames


process_camera_feed(model)
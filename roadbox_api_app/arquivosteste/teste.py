from ultralytics import YOLO
import cv2 as cv
import os

# Obtenha o caminho absoluto para o diretório atual do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Construa o caminho completo para o arquivo do modelo
model_path = os.path.join(project_dir, 'models', 'Detect-Accident.pt')
# Carregue o modelo
model = YOLO(model_path)

# Carregar a imagem com OpenCV
image_path = "closecars.png"
image = cv.imread(image_path)

if image is not None:
    # Analisar a imagem usando o método predict()
    results = model.predict(source=image, conf=0.6, iou=0.7, device='cpu', save=False)

    # Exiba os resultados detalhados
    if results and results[0].boxes is not None and len(results[0].boxes):
        print("Detecções encontradas:")
        for box in results[0].boxes:
            print(f"Classe: {int(box.cls[0])}, Confiança: {box.conf[0]}")
    else:
        print("Nenhum acidente detectado.")
else:
    print("Erro ao carregar a imagem.")

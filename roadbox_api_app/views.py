import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FrameSerializer
from .utils import analyze_frames
from ultralytics import YOLO

# Obtenha o caminho absoluto para o diretório atual do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Construa o caminho completo para o arquivo do modelo
model_path = os.path.join(project_dir, 'models', 'Detect-Accident.pt')

# Verifique se o arquivo existe antes de carregá-lo
if os.path.exists(model_path):
    model = YOLO(model_path)
    print(f"Modelo carregado com sucesso de: {model_path}")
else:
    raise FileNotFoundError(f"Arquivo de modelo não encontrado em: {model_path}")

class FrameUploadView(APIView):
    def post(self, request):
        print(request.data)
        serializer = FrameSerializer(data=request.data)
        
        if serializer.is_valid():
            frames = request.data.get('frames')  # Lista de frames
            latitude = serializer.validated_data['latitude']
            longitude = serializer.validated_data['longitude']
            dispositivo = serializer.validated_data['dispositivo']

            print(f'FRAMES ENVIADOS: {frames}')
            
            # Se 'frames' não for uma lista, coloque-o dentro de uma lista
            if not isinstance(frames, list):
                frames = [frames]
            
            # Salvar os frames
            frame_paths = self.save_frames(frames)  # Salva múltiplos frames
            
            # Analisar todos os frames
            detected_frames = analyze_frames(frames=frame_paths, longitude=longitude, latitude=latitude, model=model, dispositivo=dispositivo)
            
            return Response({
                "message": "Frames e coordenadas recebidos com sucesso!",
                "detected_frames": detected_frames,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_single_frame(self, frame):
        """Método para salvar um único frame."""
        frame_path = os.path.join('media/frames/temp', 'frame.jpg')  # Salva como frame.jpg (ou outro nome único)

        os.makedirs(os.path.dirname(frame_path), exist_ok=True)

        # Salvar o frame diretamente como um arquivo binário
        if hasattr(frame, 'chunks'):
            with open(frame_path, 'wb') as f:
                for chunk in frame.chunks():
                    f.write(chunk)
        else:
            # Caso seja um objeto `bytes`
            with open(frame_path, 'wb') as f:
                f.write(frame)
        
        return frame_path

    def save_frames(self, frames):
        """Método para salvar múltiplos frames."""
        frame_paths = []
        for i, frame in enumerate(frames, start=1):
            frame_path = os.path.join('media/frames/temp', f'frame{i}.jpg')
            os.makedirs(os.path.dirname(frame_path), exist_ok=True)
            
            # Salvar o frame diretamente como um arquivo binário
            if hasattr(frame, 'chunks'):
                with open(frame_path, 'wb') as f:
                    for chunk in frame.chunks():
                        f.write(chunk)
            else:
                # Caso seja um objeto `bytes`
                with open(frame_path, 'wb') as f:
                    f.write(frame)
            
            frame_paths.append(frame_path)

        return frame_paths

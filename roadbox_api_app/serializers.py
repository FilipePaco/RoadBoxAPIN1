from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
from rest_framework import serializers

class FrameSerializer(serializers.Serializer):
    # Defina aqui os campos para os frames
    # Exemplo:
    # Definindo o campo para múltiplos arquivos
    frames = serializers.ListField(
        child=serializers.FileField()
    )
    coordinates = serializers.CharField()

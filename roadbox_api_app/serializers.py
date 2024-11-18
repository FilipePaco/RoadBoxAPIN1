from rest_framework import serializers
from .models import EnvioDeSinistro
from django.core.exceptions import ValidationError
import re

class FrameSerializer(serializers.ModelSerializer):
    frames = serializers.ListField(
        child=serializers.ImageField(),  # Aceita múltiplas imagens
        allow_empty=False  # Não permite uma lista vazia
    )
     
    class Meta:
        model = EnvioDeSinistro
        fields = ['latitude', 'longitude', 'dispositivo', 'frames']

    def validate_latitude(self, value):
        """
        Valida a latitude para garantir que está no intervalo de -90 a 90.
        """
        if not (-90 <= value <= 90):
            raise ValidationError("Latitude deve estar entre -90 e 90.")
        return value

    def validate_longitude(self, value):
        """
        Valida a longitude para garantir que está no intervalo de -180 a 180.
        """
        if not (-180 <= value <= 180):
            raise ValidationError("Longitude deve estar entre -180 e 180.")
        return value

    def validate_dispositivo(self, value):
        """
        Valida o nome do dispositivo para garantir que siga o formato correto.
        """
        if not re.match(r'^[a-zA-Z0-9]+_\d+$', value):
            raise ValidationError("O nome do dispositivo deve seguir o padrão: <tipo_dispositivo>_<id_dispositivo>")
        return value

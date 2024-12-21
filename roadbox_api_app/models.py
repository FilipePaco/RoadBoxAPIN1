from django.db import models
import re

class EnvioDeSinistro(models.Model):
    id_envio = models.AutoField(primary_key=True)
    dispositivo = models.CharField(max_length=255)
    foto_sinistro = models.URLField()
    data_hora = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def clean(self):
        """
        Validação personalizada para garantir que o nome do dispositivo siga um padrão.
        Exemplo: 'device_type_id' (como 'camera_12345' ou 'smartphone_67890')
        """
        if not re.match(r'^[a-zA-Z0-9]+_\d+$', self.dispositivo):
            raise ValueError("O nome do dispositivo deve seguir o padrão: <tipo_dispositivo>_<id_dispositivo>")
    
    class Meta:
        db_table = 'enviodesinistro'  # Define o nome da tabela no banco de dados

from django.db import models

class EnvioDeSinistro(models.Model):
    id_envio = models.AutoField(primary_key=True)
    dispositivo = models.CharField(max_length=255)
    foto_sinistro = models.URLField()
    data_hora = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    class Meta:
        db_table = 'enviodesinistro'  # Define o nome da tabela no banco de dados

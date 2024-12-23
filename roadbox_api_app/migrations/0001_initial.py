# Generated by Django 5.1.3 on 2024-11-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnvioDeSinistro',
            fields=[
                ('id_envio', models.AutoField(primary_key=True, serialize=False)),
                ('dispositivo', models.CharField(max_length=255)),
                ('foto_sinistro', models.URLField()),
                ('data_hora', models.DateTimeField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            options={
                'db_table': 'enviodesinistro',
            },
        ),
    ]

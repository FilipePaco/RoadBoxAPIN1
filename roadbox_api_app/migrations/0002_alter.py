# Generated by Django 5.1.3 on 2024-11-17 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadbox_api_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enviodesinistro',
            name='latitude',
            field=models.DecimalField(max_digits=9, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='enviodesinistro',
            name='longitude',
            field=models.DecimalField(max_digits=9, decimal_places=6),
        ),
    ]

# Generated by Django 4.2 on 2024-05-07 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_solicitudarriendo_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='fecha_modificado',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='fecha_solicitud',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

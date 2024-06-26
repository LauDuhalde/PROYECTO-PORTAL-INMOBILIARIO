# Generated by Django 4.2 on 2024-05-03 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_inmueble_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='arrendador',
            field=models.ForeignKey(limit_choices_to={'tipo_usuario': 'arrendador'}, on_delete=django.db.models.deletion.CASCADE, related_name='inmuebles', to='web.usuario'),
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='imagen',
            field=models.ImageField(upload_to='web/media/'),
        ),
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='arrendatario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='web.usuario'),
        ),
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='inmueble',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='web.inmueble'),
        ),
    ]

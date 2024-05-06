# Generated by Django 4.2 on 2024-05-06 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_inmueble_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comunas', to='web.region')),
            ],
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inmuebles', to='web.comuna'),
        ),
    ]
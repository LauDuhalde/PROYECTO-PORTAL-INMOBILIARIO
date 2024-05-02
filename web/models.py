from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(User):
    TIPO_USUARIO_CHOICES = (
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    )
    rut = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=50, null=False, blank=False)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=13)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    
    def __str__(self) -> str:
        return (f"{self.nombres} {self.apellidos}")
    
class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = (
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela','Parcela'),
    )
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    comuna = models.CharField(max_length=50)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio = models.IntegerField()
    descripcion = models.TextField(max_length=100)
    m2_construidos = models.IntegerField()
    m2_terreno = models.IntegerField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banios = models.IntegerField()
    imagen = models.URLField(max_length=200)
    disponible = models.BooleanField(default=True)
    arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inmuebles')
    
    def __str__(self) -> str:
        return (f"{self.nombre}")
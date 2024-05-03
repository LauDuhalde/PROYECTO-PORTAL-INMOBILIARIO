from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.region})"

"""

class Usuario(User):
    TIPO_USUARIO_CHOICES = (
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    )
    rut = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=50, null=False, blank=False)
    apellidos = models.CharField(max_length=50, null=False, blank=False)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=13)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    correo_electronico = models.EmailField(unique=True, default='correo@correo.cl') 
    
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
    #comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    comuna = models.CharField(max_length=50)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    descripcion = models.TextField(max_length=100)
    m2_construidos = models.DecimalField(max_digits=10, decimal_places=2)
    m2_terreno = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_estacionamientos = models.PositiveIntegerField()
    cantidad_habitaciones = models.PositiveIntegerField()
    cantidad_banios = models.PositiveIntegerField()
    #imagen = models.URLField(max_length=200)
    imagen =models.ImageField(upload_to='web/media/')
    disponible = models.BooleanField(default=True)
    arrendador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inmuebles',limit_choices_to={'tipo_usuario': 'arrendador'})
    
    def __str__(self) -> str:
        return (f"{self.nombre}")
    
class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(Usuario, related_name='solicitudes', on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, related_name='solicitudes', on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True)
    #aprobada = models.BooleanField(default=False)
    def __str__(self):
        return f"Solicitud de {self.inmueble.nombre} por {self.arrendatario.nombres} {self.arrendatario.apellidos}"    
    
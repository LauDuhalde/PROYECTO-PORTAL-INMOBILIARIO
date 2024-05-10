from django import forms
from .models import Usuario, SolicitudArriendo
from django.contrib.auth.forms import UserChangeForm

class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono', 'correo_electronico', 'tipo_usuario']
        widgets = {
            'password': forms.PasswordInput(),
        }

class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']
        widgets = {
            'arrendatario': forms.HiddenInput(),
            'inmueble': forms.HiddenInput(),
        }

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'direccion', 'telefono', 'correo_electronico']

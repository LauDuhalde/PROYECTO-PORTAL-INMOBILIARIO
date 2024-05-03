from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from web.models import SolicitudArriendo, Inmueble, Usuario
from .forms import RegistroUsuarioForm, SolicitudArriendoForm

# Create your views here.

def index(request):
    inmuebles =  Inmueble.objects.all()
    return render(request, 'index.html',{'inmuebles':inmuebles})

@login_required
def detalle_inmueble(request, id):
    inmueble=Inmueble.objects.get(id=id)
    return render(request, 'detalle_inmueble.html',{'inmueble':inmueble})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            password = form.cleaned_data['password']
            usuario.set_password(password)
            usuario.save()
            # Autenticar al usuario después del registro
            usuario_autenticado = authenticate(username=usuario.username, password=password)
            if usuario_autenticado is not None:
                login(request, usuario_autenticado)
                # Redirigir a alguna página de éxito
                return redirect('index')  # Cambia 'inicio' a la URL deseada
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro_usuario.html', {'form': form})


def crear_solicitud_arriendo(request, inmueble_id, usuario_id):
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            # Obtener instancia del inmueble y el usuario
            inmueble = Inmueble.objects.get(pk=inmueble_id)
            usuario = Usuario.objects.get(pk=usuario_id)
            
            # Asignar los IDs al formulario y guardar la solicitud de arriendo
            solicitud = form.save(commit=False)
            solicitud.inmueble = inmueble
            solicitud.arrendatario = usuario
            solicitud.save()
            
            return redirect('success')
    else:
        form = SolicitudArriendoForm(initial={'arrendatario': usuario_id, 'inmueble': inmueble_id})
    return render(request, 'solicitud_arriendo.html', {'form': form})

def success(request):
    return render(request, 'success.html',{})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from web.models import SolicitudArriendo
from .forms import RegistroUsuarioForm

# Create your views here.

def index(request):
    return render(request, 'index.html')



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
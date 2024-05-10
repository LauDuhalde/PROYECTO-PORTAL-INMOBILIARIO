from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from web.models import SolicitudArriendo, Inmueble, Region, Comuna
from .forms import RegistroUsuarioForm, SolicitudArriendoForm, PerfilUsuarioForm, InmuebleForm

def obtener_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(region_id=region_id).values('id', 'nombre')
    return JsonResponse(list(comunas), safe=False)

def index(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all()
    inmuebles = Inmueble.objects.filter(disponible=True)  # Obtener todos los inmuebles disponibles por defecto o filtrar según tus necesidades
    
    # Lógica para filtrar inmuebles por región y comuna si se han seleccionado
    region_id = request.GET.get('region')
    comuna_id = request.GET.get('comuna')
    selected_region = None
    if region_id:
        selected_region = Region.objects.get(pk=region_id)
        if not comuna_id:
            inmuebles = Inmueble.objects.filter(comuna__region=selected_region)
        else:
            inmuebles = Inmueble.objects.filter(comuna_id=comuna_id)
    
    return render(request, 'index.html', {'regiones': regiones, 'comunas': comunas, 'inmuebles': inmuebles, 'selected_region': selected_region})

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


def crear_solicitud_arriendo(request, inmueble_id):
    # Obtener instancia del inmueble y el usuario
    inmueble = Inmueble.objects.get(pk=inmueble_id)
    usuario = request.user.usuario
            
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            # Asignar los IDs al formulario y guardar la solicitud de arriendo
            solicitud = form.save(commit=False)
            solicitud.inmueble = inmueble
            solicitud.arrendatario = usuario
            solicitud.save()
            
            return redirect('success')
    else:
        form = SolicitudArriendoForm(initial={'arrendatario': usuario.id, 'inmueble': inmueble.id})
    return render(request, 'solicitud_arriendo.html', {'form': form, 'usuario':usuario, 'inmueble':inmueble})

def success(request):
    return render(request, 'success.html',{})

def mi_perfil(request):
    usuario = request.user.usuario
    inmuebles_y_solicitudes = None
    solicitudes_arrendatario = None
    if usuario.tipo_usuario == 'arrendador':
        # Consultar todos los inmuebles del usuario
        inmuebles_arrendador = Inmueble.objects.filter(arrendador=usuario)

        # Inicializar una lista para almacenar los inmuebles y sus solicitudes asociadas
        inmuebles_y_solicitudes = []

        # Iterar sobre los inmuebles del usuario
        for inmueble in inmuebles_arrendador:
            # Consultar todas las solicitudes asociadas a este inmueble
            solicitudes = SolicitudArriendo.objects.filter(inmueble=inmueble)
            
            # Agregar el inmueble y sus solicitudes asociadas a la lista
            inmuebles_y_solicitudes.append({
                'inmueble': inmueble,
                'solicitudes': solicitudes
            })
    else:
        # Consultar todas las solicitudes de arriendo realizadas por el arrendatario
        solicitudes_arrendatario = SolicitudArriendo.objects.filter(arrendatario=usuario)
    return render(request,'mi_perfil.html',{'inmuebles_y_solicitudes':inmuebles_y_solicitudes, 'solicitudes_arrendatario':solicitudes_arrendatario})

def editar_perfil(request):
    usuario = request.user.usuario
    
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tus datos se han actualizado correctamente.')
            return redirect('mi_perfil')
    else:
        form = PerfilUsuarioForm(instance=usuario)
    
    return render(request, 'editar_perfil.html', {'form': form})


##Código profe

def crear_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.propietario = request.user.usuario
            inmueble.save()
            return redirect('index') 
    else:
        form = InmuebleForm()
    return render(request, 'alta_inmueble.html', {'form': form})


@login_required
def actualizar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, pk=id)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = InmuebleForm(instance=inmueble)
    return render(request, 'editar_inmueble.html',{'form':form })
        
@login_required
def eliminar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, pk=id)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('index')
    else:
        return render(request,'eliminar_inmueble.html', {'inmueble':inmueble} )
        
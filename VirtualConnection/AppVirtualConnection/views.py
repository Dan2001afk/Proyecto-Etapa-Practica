from django.shortcuts import render, redirect
from .forms import CultivoForm
from AppVirtualConnection.Cultivos import guardar_cultivo
import requests
from .viewsLogin import login_required
from django.contrib.auth import logout
from firebase_admin import auth
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .firebase_config import *

#Plantillas Publicas

# def Contacto(request):
#     return render (request, "VistasPublicas/Contacto.html")

def Inicio(request):
    return render (request, "VistasPublicas/Inicio.html")

# def Nosotros(request):
#     return render (request, "VistasPublicas/Nosotros.html")

# def Noticias(request):
#     return render (request, "VistasPublicas/Noticias.html")

# def Servicios(request):
#     return render (request, "VistasPublicas/Servicios.html")

#plantillas para usuario logueado

@login_required
def Alarmas(request):
    return render (request, "Usuarios/Alarmas.html")

@login_required
def Tableros(request):
    return render (request, "Usuarios/Tableros.html")

@login_required
def Productos(request):
    return render (request, "Usuarios/Productos.html")

@login_required
def Dispositivos(request):
    return render(request, 'Usuarios/Dispositivos.html')


@login_required
def Estadisticas(request):
    if request.method == 'POST':
        # Aquí recibes el nombre de usuario de Firebase
        username = request.POST.get('username')
        # Pasa el nombre de usuario a la plantilla
        return render(request, 'Usuarios/Estadisticas.html', {'username': username})
    else:
        return render(request, 'Usuarios/Estadisticas.html')

# plantillas de Autenticacion
from django.shortcuts import render

def reset_password_success(request):
    return render(request, 'Autenticacion/Envio_Correo_Restablecer_Exitoso.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return render(request, 'Autenticacion/IniciarSesion.html') 


#------------------------------------------------------PRUEBAS---------------------------------------------------------


def Dashboard(request):
    if request.method == 'POST':
        form = CultivoForm(request.POST)
        if form.is_valid():
            # Crear un nuevo documento en Firebase Firestore con los datos del formulario
            nuevo_cultivo = {
                'nombre': form.cleaned_data['nombre'],
                'ubicacion': form.cleaned_data['ubicacion'],
                'variedad': form.cleaned_data['variedad'],
                'Temperatura_suelo': form.cleaned_data['temperatura_suelo'],
                'Humedad': form.cleaned_data['humedad']
            }
            db.collection('Cultivos').add(nuevo_cultivo)
            
            # Redireccionar a otra página después de guardar los datos
            return redirect('Dashboard')
    else:
        form = CultivoForm()
        
    return render(request, 'Usuarios/Dashboard.html', {'form': form})
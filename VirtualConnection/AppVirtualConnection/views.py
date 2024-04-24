from typing import Any
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
from firebase_admin import storage

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
    user_info = request.session.get('user_info')
    
    if user_info:
        return render (request, "Usuarios/Alarmas.html",{'user_info':user_info})

@login_required
def Tableros(request):
    user_info = request.session.get('user_info')
    
    if user_info:
        return render (request, "Usuarios/Tableros.html",{'user_info':user_info})

@login_required
def Productos(request):
    user_info = request.session.get('user_info')
    
    if user_info:
        return render (request, "Usuarios/Productos.html",{'user_info':user_info})

# @login_required
# def Dispositivos(request):
#     return render(request, 'Usuarios/Dispositivos.html')


@login_required
def Estadisticas(request):
    user_info = request.session.get('user_info')
    
    if user_info:
        
        return render(request, 'Usuarios/Estadisticas.html',{'user_info':user_info})

# plantillas de Autenticacion
from django.shortcuts import render

def reset_password_success(request):
    return render(request, 'Autenticacion/Envio_Correo_Restablecer_Exitoso.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return render(request, 'Autenticacion/IniciarSesion.html') 


#------------------------------------------------------PRUEBAS---------------------------------------------------------


def Dashboard(request):
    user_info = request.session.get('user_info')
    
    if user_info:
        if request.method == 'POST':
            form = CultivoForm(request.POST, request.FILES)
            print("Datos del formulario",CultivoForm)
            if form.is_valid():
                nuevo_cultivo = {
                    'nombre': form.cleaned_data['nombre'],
                    'ubicacion': form.cleaned_data['ubicacion'],
                    'variedad': form.cleaned_data['variedad'],
                    'Temperatura_suelo': form.cleaned_data['temperatura_suelo'],
                    'Humedad': form.cleaned_data['humedad']
                }
                
                # Guardar la imagen en Firebase Storage
                imagen = request.FILES['imagen']
                bucket = storage.bucket()  # Obtener el bucket predeterminado
                blob = bucket.blob(imagen.name)  # Crear un nuevo blob en el bucket con el nombre del archivo
                blob.upload_from_file(imagen)  # Subir la imagen al blob
                
                # Obtener la URL de descarga de la imagen en Firebase Storage
                imagen_url = blob.public_url
                
                # Agregar la URL de la imagen al diccionario del nuevo cultivo
                nuevo_cultivo['imagen_url'] = imagen_url
                
                # Guardar el nuevo cultivo en la base de datos Firestore o en donde lo desees
                # db.collection('Cultivos').add(nuevo_cultivo)
                
                return redirect('Dashboard')
        else:
            form = CultivoForm()
        
        return render(request, 'Usuarios/Dashboard.html', {'user_info': user_info, 'form': form})
    
    return redirect('login')


def Dispositivos(request):
    user_info = request.session.get('user_info')
    
    if user_info:
        db = firestore.client()
        cultivos_ref = db.collection('Cultivos')
        cultivos_docs = cultivos_ref.get()

        cultivos_data = []
        for cultivo in cultivos_docs:
            cultivo_data = cultivo.to_dict()
            cultivos_data.append(cultivo_data)
    return render(request, 'Usuarios/Dispositivos.html', {'cultivos': cultivos_data, 'user_info':user_info})
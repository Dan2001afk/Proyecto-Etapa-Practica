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


from firebase_admin import storage

import firebase_admin
from firebase_admin import credentials, storage
from django.shortcuts import redirect, render
from .forms import CultivoForm

from firebase_admin import firestore
from django.shortcuts import render, redirect
from .forms import CultivoForm  # Importa tu formulario aquí

@login_required
def Dashboard(request):
    user_info = request.session.get('user_info')
    db = firestore.client()
    cultivos_ref = db.collection('Cultivos')
    cultivos_docs = cultivos_ref.get()
    cultivos_data = []
    for cultivo_doc in cultivos_docs:
        cultivo_data = cultivo_doc.to_dict()
        cultivo_id = cultivo_doc.id
        imagen_url = cultivo_data.get('imagen_url', '')  # Obtener la URL de la imagen del documento
        print("url de la imagen", imagen_url)
        cultivo_data['imagen_url'] = imagen_url  # Agregar la URL de la imagen al diccionario de datos del cultivo
        cultivos_data.append({'id': cultivo_id, 'data': cultivo_data})  # Agregar el ID del documento y los datos del cultivo a la lista
        print("Datos del cultivo", cultivos_data)
    if user_info:
        if request.method == 'POST':
            form = CultivoForm(request.POST, request.FILES)
            if form.is_valid():
                # Crear un nuevo objeto Cultivo con los datos del formulario
                nuevo_cultivo = {
                    'nombre': form.cleaned_data['nombre'],
                    'ubicacion': form.cleaned_data['ubicacion'],
                    'variedad': form.cleaned_data['variedad'],
                    'Temperatura_suelo': form.cleaned_data['temperatura_suelo'],
                    'Humedad': form.cleaned_data['humedad']
                }
                
                # Verificar si se ha subido una imagen
                if 'imagen' in request.FILES:
                    # Guardar la imagen en Firebase Storage
                    imagen = request.FILES['imagen']
                    bucket = storage.bucket()  
                    blob = bucket.blob(imagen.name) 
                    blob.upload_from_file(imagen)  
                    
                    # Obtener la URL de descarga de la imagen en Firebase Storage
                    imagen_url = blob.public_url
                    
                    # Agregar la URL de la imagen al diccionario del nuevo cultivo
                    nuevo_cultivo['imagen_url'] = imagen_url
                
                # Guardar el nuevo cultivo en la base de datos Firestore
                db = firestore.client()
                db.collection('Cultivos').add(nuevo_cultivo)
                
                return redirect('Dashboard')  # Redirigir al dashboard después de guardar el formulario
        
        else:
            form = CultivoForm()
        
        return render(request, 'Usuarios/Dashboard.html', {'cultivos': cultivos_data,'user_info': user_info, 'form': form})
    
    return redirect('login')


@login_required
def Dispositivos(request):
    user_info = request.session.get('user_info')
    db = firestore.client()
    cultivos_ref = db.collection('Cultivos')
    cultivos_docs = cultivos_ref.get()

    cultivos_data = []
    for cultivo_doc in cultivos_docs:
        cultivo_data = cultivo_doc.to_dict()
        cultivo_id = cultivo_doc.id
        imagen_url = cultivo_data.get('imagen_url', '')  # Obtener la URL de la imagen del documento
        print("url de la imagen", imagen_url)
        cultivo_data['imagen_url'] = imagen_url  # Agregar la URL de la imagen al diccionario de datos del cultivo
        cultivos_data.append({'id': cultivo_id, 'data': cultivo_data})  # Agregar el ID del documento y los datos del cultivo a la lista
        print("Datos del cultivo", cultivos_data)
    return render(request, 'Usuarios/Dispositivos.html', {'cultivos': cultivos_data,'user_info': user_info,})
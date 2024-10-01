import time
from typing import Any
from AppVirtualConnection.models import Alerta
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
import os
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, storage
from django.shortcuts import redirect, render
from firebase_admin import firestore
from .forms import CultivoForm  # Importa tu formulario aquí
from decouple import config

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
    
    db = firestore.client()
    alertas_ref = db.collection('alertas')
    alertas = alertas_ref.stream()

    lista_alertas = []
    for alerta in alertas:
        alert_data = alerta.to_dict()
        lista_alertas.append(Alerta(
            id=alerta.id,
            mensaje=alert_data.get('mensaje'),
            tipo=alert_data.get('tipo'),
            fecha=alert_data.get('fecha')
        ))

    if user_info:
        return render (request, "Usuarios/Alarmas.html",{'user_info':user_info, 'alertas': lista_alertas})

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



@login_required
def Dashboard(request):
    user_info = request.session.get('user_info')

    intervalo_generacion_reportes = config('INTERVALO_GENERACION_REPORTES', default=60000, cast=int)  # valor por defecto
    intervalo_actualizacion_grafica = config('INTERVALO_ACTUALIZACION_GRAFICA', default=5000, cast=int)  # valor por defecto
    if user_info:
        user_uid = user_info.get('uid')  # Obtener el UID del usuario autenticado
        
        print("usuario autenticado",user_uid)

        db = firestore.client()
        
        # Consulta los cultivos filtrados por el UID del usuario autenticado
        cultivos_ref = db.collection('Cultivos').where('user_uid', '==', user_uid)
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
        
        if request.method == 'POST':
            form = CultivoForm(request.POST, request.FILES)
            if form.is_valid():
                # Crear un nuevo objeto Cultivo con los datos del formulario
                nuevo_cultivo = {
                    'nombre': form.cleaned_data['nombre'],
                    'ubicacion': form.cleaned_data['ubicacion'],
                    'variedad': form.cleaned_data['variedad'],
                    'Temperatura_suelo': form.cleaned_data['temperatura_suelo'],
                    'Humedad': form.cleaned_data['humedad'],
                    'user_uid': user_uid  # Asociar el cultivo con el UID del usuario autenticado
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
                db.collection('Cultivos').add(nuevo_cultivo)
                
                return redirect('Dashboard')  # Redirigir al dashboard después de guardar el formulario
        
        else:
            form = CultivoForm()
        
        return render(request, 'Usuarios/Dashboard.html', {'cultivos': cultivos_data, 
            'user_info': user_info, 
            'form': form, 
            'intervalo_generacion_reportes': intervalo_generacion_reportes,
            'intervalo_actualizacion_grafica': intervalo_actualizacion_grafica})
    
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

import requests
from django.shortcuts import render

API_KEY = 'fc79abf6af264a718b0214146241707'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

def get_weather(city):
    params = {
        'key': API_KEY,
        'q': city,
        'lang': 'es',
        'aqi': 'no'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        print(f"Error fetching data for {city}: {data.get('error', 'Unknown error')}")
        return None


def ClimaBogota(request):
    user_info = request.session.get('user_info')
    city = 'Bogotá'
    weather_data = get_weather(city)

    if weather_data and 'current' in weather_data:
        weather = {
            'city': city,
            'temperature': weather_data['current']['temp_c'],
            'description': weather_data['current']['condition']['text'],
            'icon': weather_data['current']['condition']['icon']
        }
    else:
        weather = None
        print(f"Could not retrieve weather for {city}")

    return render(request, 'Usuarios/Estadisticas.html', {'weather': weather, 'user_info':user_info})



from django.shortcuts import render
from firebase_admin import firestore

# copiar direccion de la carpeta correcta
RUTA_GUARDAR_JSON = os.path.join('C:/Users/Daniel Gonzalez/Desktop/Proyecto-Etapa-Practica/VirtualConnection/AppVirtualConnection/static/json')


@csrf_exempt
def guardar_json(request):
    if request.method == 'POST':
        try:
            # Obtener los datos enviados desde el cliente
            datos = json.loads(request.body)
            cultivo_id = datos.get('cultivo')
            temperatura = datos.get('temperatura')
            humedad = datos.get('humedad')
            timestamp = datos.get('timestamp')

            if not cultivo_id:
                return JsonResponse({'error': 'Falta el ID del cultivo'}, status=400)

            # Crear o actualizar el archivo JSON para el cultivo
            nombre_archivo = f"{cultivo_id}.json"
            ruta_completa = os.path.join(RUTA_GUARDAR_JSON, nombre_archivo)

            # Cargar el contenido existente del archivo (si lo hay)
            if os.path.exists(ruta_completa):
                with open(ruta_completa, 'r') as archivo_json:
                    datos_existentes = json.load(archivo_json)
            else:
                datos_existentes = []

            # Agregar el nuevo reporte al JSON
            nuevo_reporte = {
                'temperatura': temperatura,
                'humedad': humedad,
                'timestamp': timestamp
            }
            datos_existentes.append(nuevo_reporte)

            # Guardar el archivo JSON actualizado
            with open(ruta_completa, 'w') as archivo_json:
                json.dump(datos_existentes, archivo_json, indent=4)

            return JsonResponse({'mensaje': 'Reporte guardado correctamente'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Error al guardar el archivo: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)






#ACTUALIZA CULTIVOS
def actualizar_cultivo(request, cultivo_id):
    
    cultivo_ref = db.collection('Cultivos').document(cultivo_id)
    
    if request.method == 'POST':
        # Crear un formulario con los datos enviados
        form = CultivoForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Actualizar los campos del cultivo
            cultivo_ref.update({
                'nombre': form.cleaned_data['nombre'],
                'ubicacion': form.cleaned_data['ubicacion'],
                'variedad': form.cleaned_data['variedad'],
                'temperatura_suelo': form.cleaned_data['temperatura_suelo'],
                'humedad': form.cleaned_data['humedad'],
            })

            
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                bucket = storage.bucket()
                blob = bucket.blob(imagen.name)
                blob.upload_from_file(imagen)

                
                imagen_url = blob.public_url

                
                cultivo_ref.update({
                    'imagen_url': imagen_url,
                })

            # Devuelve una respuesta JSON para manejar el cierre del modal y actualizar la vista
            return JsonResponse({'success': True})

        # Si el formulario no es válido, imprime los errores
        print(form.errors)

    # Si no es una solicitud POST, devolver un error
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def eliminar_cultivo(request, cultivo_id):
    if request.method == 'DELETE':
        # Elimina el cultivo de Firestore
        cultivo_ref = db.collection('Cultivos').document(cultivo_id)
        cultivo_ref.delete()  # Elimina el documento

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
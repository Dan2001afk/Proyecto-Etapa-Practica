from django.shortcuts import render, redirect
from .forms import CultivoForm
from .Cultivos import guardar_cultivo
import requests


#Plantillas Publicas

def Contacto(request):
    return render (request, "VistasPublicas/Contacto.html")

def Inicio(request):
    return render (request, "VistasPublicas/Inicio.html")

def Nosotros(request):
    return render (request, "VistasPublicas/Nosotros.html")

def Noticias(request):
    return render (request, "VistasPublicas/Noticias.html")

def Servicios(request):
    return render (request, "VistasPublicas/Servicios.html")

#plantillas para usuario logueado

def Dashboard(request, username):
    return render(request, 'Usuarios/dashboard.html', {'username': username})

def Alarmas(request):
    return render (request, "Usuarios/Alarmas.html")

def Tableros(request):
    return render (request, "Usuarios/Tableros.html")

def Productos(request):
    return render (request, "Usuarios/Productos.html")

def Dispositivos(request):
    return render(request, 'Usuarios/Dispositivos.html')

def Estadisticas(request):
    return render(request, 'Usuarios/Estadisticas.html')

# plantillas de Autenticacion
from django.shortcuts import render

def reset_password_success(request):
    return render(request, 'Autenticacion/Envio_Correo_Restablecer_Exitoso.html')

def CerrarSesion(request):
    return render (request, "Autenticacion/CerrarSesion.html")


#------------------------------------------------------PRUEBAS---------------------------------------------------------



def agregar_cultivo(request):
    if request.method == 'POST':
        form = CultivoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            ubicacion = form.cleaned_data['ubicacion']
            variedad = form.cleaned_data['variedad']
            guardar_cultivo(nombre, ubicacion, variedad)  # Llama a la función para guardar en Firebase
            print("error en envio de formulario",form)
            return redirect('dashboard')  # Redirige a la página de éxito después de guardar
    else:
        form = CultivoForm()
    return render(request, 'Usuarios/Dashboard.html', {'form': form})


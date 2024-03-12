from django.shortcuts import render


#Plantilla de inicio
def Inicio(request):
    return render (request, "Inicio.html")

#plantillas para usuario logueado
from django.shortcuts import render

def Dashboard(request, username):
    return render(request, 'dashboard.html', {'username': username})

def indexx(request):
    return render(request, 'gridstack.html')


def Alarmas(request):
    return render (request, "Alarmas.html")

def Tableros(request):
    return render (request, "Tableros.html")

def Productos(request):
    return render (request, "Productos.html")

def Dispositivos(request):
    return render(request, 'Dispositivos.html')

def Estadisticas(request):
    return render(request, 'Estadisticas.html')

# plantilla para cerrar sesion
def CerrarSesion(request):
    return render (request, "CerrarSesion.html")

#------------------------------------------------------PRUEBAS---------------------------------------------------------




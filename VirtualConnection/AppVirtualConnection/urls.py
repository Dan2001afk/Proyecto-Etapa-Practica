from django.urls import path
from .views import *
from .viewsLogin import *
from . import views
from . import viewsLogin
from django.conf import settings 
from django.conf.urls.static import static 


urlpatterns=[
        
        path('',Inicio,name="InicioPage"),
        path('Inicio',Inicio,name="InicioPage"),
        path('dashboard/<str:username>/', views.Dashboard, name='Dashboard'),
        path('Dispositivos/',Dispositivos,name="DispositivosPage"),
        path('Estadisticas/',Estadisticas,name="EstadisticasPage"),
        path('Alarmas/',Alarmas,name="AlarmasPage"),
        path('Tableros/',Tableros,name="TablerosPage"),
        path('Productos/',Productos,name="ProductosPage"),


        #Autenticacion
        path('IniciarSesion/', viewsLogin.login_firebase, name='login'),
        path('RegistrarUsuarios/', viewsLogin.registro_usuario, name='Registro'),
        
        #recuperacion de contraseña
        path('reset-password/', reset_password_view, name='Reset-passwordPage'),
        
        #prueba Gridstack

        path('pruebaindexx/', views.indexx, name='indexx'),
        
        #cerrar sesion
        path('CerrarSesion/', Inicio, name='panel1'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

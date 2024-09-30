from django.urls import path
from .views import *
from .viewsLogin import *
from . import views
from . import viewsLogin
from django.conf import settings 
from django.conf.urls.static import static 



urlpatterns=[
        
        # Vistas Publicas
        path('',Inicio,name="InicioPage"),
        path('Inicio',Inicio,name="InicioPage"),
        # path('Contacto',Contacto,name="ContactoPage"),
        # path('Nosotros',Nosotros,name="NosotrosPage"),
        # path('Noticias',Noticias,name="NoticiasPage"),
        # path('Servicios',Servicios,name="NoticiasPage"),

        # Vistas Usuarios
        path('Dashboard/', views.Dashboard, name='Dashboard'),
        path('Dispositivos',Dispositivos,name="DispositivosPage"),
        path('Clima/', views.ClimaBogota, name='clima_bogota'),
        path('Alarmas',Alarmas,name="AlarmasPage"),
        path('Tableros',Tableros,name="TablerosPage"),
        path('Productos',Productos,name="ProductosPage"),
        # Vistas Autenticacion
        path('IniciarSesion/', viewsLogin.login_firebase, name='login'),
        path('RegistrarUsuarios/', viewsLogin.registro_usuario, name='Registro'),
        path('reset_password_success/', reset_password_success, name='reset_password_success'),
        path('reset-password/', Restablecer_Contraseña, name='Reset-passwordPage'),
        path('logout/', logout_view, name='logout'),  # URL para cerrar sesión
        
        #Guardar Json
        path('guardar-json/', guardar_json, name='guardar_json'),
        
        

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

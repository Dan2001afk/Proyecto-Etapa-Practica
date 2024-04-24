#LOGICA PARA REGISTRO DE USUARIOS Y LOGEO
from .forms import *
from django.shortcuts import render, redirect
import json
import requests
from .forms import RegistroForm
from firebase_admin import auth
from firebase_admin import firestore
from .firebase_config import *



def login_firebase(request):
    error_message = ""
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA"
        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(auth_url, json=data)

        if response.status_code == 200:
            user_data = response.json()
            user_uid = user_data.get('localId')
            
            # Consulta la colección 'users' en Firestore para obtener el nombre de usuario
            db = firestore.client()
            user_ref = db.collection('users').document(user_uid)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                user_info = {
                    'username': user_doc.get('username'),
                    'photo_url': user_data.get('photoUrl', '/static/perfil.png') 
                }
                
                request.session['user_info'] = user_info
                print("user_info:", user_info)
                
                # Redirige a la página de dashboard después del inicio de sesión
                #return render(request, 'Usuarios/Dashboard.html',{'user_info':user_info})
                return redirect ('Dashboard')
            else:
                error_message = "Datos del usuario no encontrados en la base de datos"
        else:
            error_message = response.json().get('error', {}).get('message', 'Error de autenticación')

    return render(request, 'Autenticacion/IniciarSesion.html', {'error_message': error_message})


# Decorador personalizado para verificar la autenticación del usuario

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
    
        if 'user_info' not in request.session:
            # Si no hay información del usuario en la sesión, envia el usuario a la vista de iniciar sesion 
            return render(request, 'Autenticacion/IniciarSesion.html')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper



def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']

            auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA"
            data = {"email": email, "password": password, "returnSecureToken": True}

            response = requests.post(auth_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data['localId']

                # Guardar username en Firestore
                user_info = {"email": email, "username": username}
                db.collection('users').document(user_id).set(user_info)

                return redirect('login')
            else:
                error_message = response.json().get('error', {}).get('message', 'Error de registro')
                return render(request, 'Autenticacion/Registro.html', {'error_message': error_message})
    else:
        form = RegistroForm()

    return render(request, 'Autenticacion/Registro.html', {'form': form})





#recuperar contraseña

import requests
from django.http import JsonResponse
from django.shortcuts import render

# Función para enviar la solicitud de restablecimiento de contraseña a Firebase
def reset_password_firebase(email):
    api_key = 'AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA'
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'

    data = {
        'requestType': 'PASSWORD_RESET',
        'email': email,
    }
    response = requests.post(url, json=data)

    if response.ok:
        print('Correo electrónico de restablecimiento de contraseña enviado con éxito')
        return {'success': True, 'message': 'Correo electrónico de restablecimiento de contraseña enviado con éxito'}
    else:
        print(f'Error al enviar el correo electrónico de restablecimiento de contraseña: {response.text}')
        return {'success': False, 'error_message': f'Error al enviar el correo electrónico de restablecimiento de contraseña: {response.text}'}

# Vista de Django para el restablecimiento de contraseña
def Restablecer_Contraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Llama a la función para restablecer la contraseña en Firebase
        reset_password_firebase(email)

        # Redirige al usuario a la página de éxito
        return redirect('reset_password_success')

    return render(request, 'Autenticacion/Restablecer_Contraseña.html')

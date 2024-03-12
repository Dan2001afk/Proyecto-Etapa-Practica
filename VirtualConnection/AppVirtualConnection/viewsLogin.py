#VISTAS PARA REGISTRO DE USUARIOS Y LOGEO
from .forms import *
from firebase_admin import credentials
from django.shortcuts import render, redirect
import json
import requests
from .forms import RegistroForm
from firebase_admin import auth
from django.http import JsonResponse
from firebase_admin import firestore
from .firebase_config import *

# Asegúrate de importar el formulario adecuado



from django.shortcuts import redirect

def login_firebase(request):
    error_message = ""
    username = ""  # Inicializamos el nombre de usuario como una cadena vacía
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # ENVIAMOS LA  SOLICITUD A LA API REST DE  FIREBASE PARA LOGUEAR EL USUARIO
        auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA"  # Reemplaza API_KEY con tu clave API de Firebase

        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(auth_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            user_data = response.json()
            # Si la solicitud tiene un estado de 200, el inicio de sesión fue exitoso
            # Obtenemos el UID del usuario autenticado
            user_uid = user_data.get('localId')
            # Aquí puedes realizar cualquier operación adicional que necesites con el UID del usuario
            # Por ejemplo, buscar datos específicos del usuario en Firestore
            user_ref = db.collection('users').document(user_uid)
            user_doc = user_ref.get()
            if user_doc.exists:
                user_info = user_doc.to_dict()
                username = user_info.get('username', 'Usuario sin nombre')  # Obtenemos el nombre de usuario del documento
                # Si todo está bien, redirigimos al usuario a la página de Dashboard y pasamos el nombre de usuario como parte del contexto
                return redirect('Dashboard', username=username)
            else:
                # Si el documento del usuario no existe en Firestore, puedes manejarlo como desees
                error_message = "Datos del usuario no encontrados"
        else:
            # Si la solicitud no tiene un estado de 200, hubo un error de inicio de sesión
            # Obtén el mensaje de error de la respuesta
            error_message = response.json().get('error', {}).get('message', 'Error de autenticación')

    # Retornamos al la vista del formulario y mostramos el error 
    return render(request, 'login.html', {'error_message': error_message})






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
                return render(request, 'register.html', {'error_message': error_message})
    else:
        form = RegistroForm()

    return render(request, 'register.html', {'form': form})





#recuperar contraseña

import requests
from django.http import JsonResponse
from django.shortcuts import render

# Función para enviar la solicitud de restablecimiento de contraseña a Firebase
def reset_password_firebase(email):
    # Reemplaza 'API_KEY' con la clave de la API de tu proyecto Firebase
    api_key = 'AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA'
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'

    # Cuerpo de la solicitud para restablecer la contraseña
    data = {
        'requestType': 'PASSWORD_RESET',
        'email': email,
    }

    # Realiza la solicitud a la API REST de Firebase
    response = requests.post(url, json=data)

    # Procesa la respuesta
    if response.ok:
        print('Correo electrónico de restablecimiento de contraseña enviado con éxito')
        return {'success': True, 'message': 'Correo electrónico de restablecimiento de contraseña enviado con éxito'}
    else:
        print(f'Error al enviar el correo electrónico de restablecimiento de contraseña: {response.text}')
        return {'success': False, 'error_message': f'Error al enviar el correo electrónico de restablecimiento de contraseña: {response.text}'}

# Vista de Django para el restablecimiento de contraseña
def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        # Llama a la función para restablecer la contraseña en Firebase
        reset_password_firebase(email)

        # Devuelve una respuesta JSON
        return JsonResponse({'success': True, 'message': 'Solicitud de restablecimiento de contraseña exitosa. Verifica tu correo electrónico.'})

    return render(request, 'reset_password.html')

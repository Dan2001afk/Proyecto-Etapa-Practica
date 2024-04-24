import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la aplicación Firebase con las credenciales
cred = credentials.Certificate("C:/Users/camilo/Desktop/sena/Proyecto-Etapa-Practica/VirtualConnection/AppVirtualConnection/virtualconnection.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/',
        'storageBucket': 'cultivos_virtual_connections'
    })

db = firestore.client()

import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la aplicación Firebase con las credenciales

cred = credentials.Certificate("C:/Users/Daniel Gonzalez/Desktop/Proyecto-Etapa-Practica/VirtualConnection/AppVirtualConnection/virtualconnection.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/',
        'storageBucket': 'virtualconnection-643e6.appspot.com'
    })

db = firestore.client()

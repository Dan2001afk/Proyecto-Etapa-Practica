import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth


# Inicializa la aplicación Firebase con las credenciales
cred = credentials.Certificate("C:/Users/camilo/Desktop/ProyectoFinalEtapaPractica/VirtualConnection/AppVirtualConnection/virtualconnection.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/'
    })

db = firestore.client()

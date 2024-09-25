import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la aplicación Firebase con las credenciales
<<<<<<< HEAD
cred = credentials.Certificate("C:/Users/Daniel Gonzalez/Downloads/Proyecto-Etapa-Practica/VirtualConnection/AppVirtualConnection/virtualconnection.json")
=======
cred = credentials.Certificate("C:/Users/Daniel Gonzalez/Desktop/Proyecto-Etapa-Practica/VirtualConnection/AppVirtualConnection/virtualconnection.json")
>>>>>>> 992540d4 (configuracion para que la graficas tomen los valores de las temperaturas desde archivo JSON)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://virtualconnection-643e6-default-rtdb.firebaseio.com/',
        'storageBucket': 'virtualconnection-643e6.appspot.com'
    })

db = firestore.client()

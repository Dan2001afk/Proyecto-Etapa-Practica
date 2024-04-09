import firebase_admin
from firebase_admin import credentials, firestore
from .firebase_config import *


db = firestore.client()

# Guardar datos en Firebase
def guardar_cultivo(nombre, ubicacion, variedad,Temperatura_suelo,Humedad):
    # Obtener una referencia a la colección 'Cultivos' en Firebase
    cultivos_ref = db.collection('Cultivos')
    
    # Crear un nuevo documento con un ID generado automáticamente
    nuevo_cultivo_ref = cultivos_ref.document()

    # Guardar los datos en el documento
    nuevo_cultivo_ref.set({
        'nombre': nombre,
        'ubicacion': ubicacion,
        'Temperatura_suelo': Temperatura_suelo,
        'Humedad' : Humedad,
        'variedad': variedad,
    })
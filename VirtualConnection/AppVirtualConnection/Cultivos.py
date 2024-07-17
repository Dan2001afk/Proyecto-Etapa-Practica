import firebase_admin
from firebase_admin import credentials, firestore
from .firebase_config import *


db = firestore.client()

    # Guardar datos en  base de datos de Firebase
def guardar_cultivo(nombre, ubicacion, variedad,Temperatura_suelo,Humedad):
    # De esta forma obtenemos una referencia a la colección 'Cultivos' en Firebase
    cultivos_ref = db.collection('Cultivos')
    
    #Creamos documentos con ids generados automaticamente 
    nuevo_cultivo_ref = cultivos_ref.document()

    # Guardamos los datos en el documento de la colección Cultivos
    nuevo_cultivo_ref.set({
        'nombre': nombre,
        'ubicacion': ubicacion,
        'Temperatura_suelo': Temperatura_suelo,
        'Humedad' : Humedad,
        'variedad': variedad,
    })
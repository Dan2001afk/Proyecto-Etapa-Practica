from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from firebase_admin import auth as firebase_auth
import firebase_admin
from firebase_admin import credentials


class CustomUser(AbstractUser):
    uid = models.CharField(max_length=255, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.uid:
            self.uid = self.uid
        elif self.id:
            self.uid = self.id
        else:
            self.uid = None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.uid:
            user = firebase_auth.get_user(self.uid)
            if not user:
                user = firebase_auth.create_user(uid=self.uid)
            firebase_auth.update_user(
                self.uid,
                email=self.email,
                display_name=self.username,
                phone_number=self.phone_number,
            )

class Alerta:
    def __init__(self, id, mensaje, tipo, fecha):
        self.id = id
        self.mensaje = mensaje
        self.tipo = tipo
        self.fecha = fecha

    def guardar_en_firebase(self):
        # Acceder a Firestore o Realtime Database
        db = firebase_admin.firestore.client()
        db.collection('alertas').document(self.id).set({
            'mensaje': self.mensaje,
            'tipo': self.tipo,
            'fecha': self.fecha
        })

from django import forms

class RegistroForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# class InsertarCultivos(forms.Form):
#     Nombre= forms.CharField(label="Nombre")
#     Ubicacion = forms.CharField(label="Ubicacion")
#     Variedad = forms.CharField(label="variedad")

class CultivoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    ubicacion = forms.CharField(max_length=100)
    variedad = forms.CharField(max_length=100)
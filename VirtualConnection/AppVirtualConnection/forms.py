from django import forms

class GraficaForm(forms.Form):
    dato_x = forms.CharField(label="Dato X")
    dato_y = forms.CharField(label="Dato Y")

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
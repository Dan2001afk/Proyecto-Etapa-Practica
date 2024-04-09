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


from django import forms

class CultivoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    ubicacion = forms.CharField(max_length=100)
    variedad = forms.CharField(max_length=100)
    temperatura_suelo = forms.FloatField()
    humedad = forms.FloatField()

    def __init__(self, *args, **kwargs):
        cultivos = kwargs.pop('cultivos', None)  # Obtiene la lista de cultivos del argumento kwargs
        super().__init__(*args, **kwargs)  # Llama al constructor de la clase base

        if cultivos:
            # Si se proporciona la lista de cultivos, la usa para rellenar el campo de selección
            self.fields['cultivo'] = forms.ChoiceField(choices=[(cultivo['nombre'], cultivo['nombre']) for cultivo in cultivos])

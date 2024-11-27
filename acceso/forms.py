from django import forms

class LoginForm(forms.Form):
    run = forms.CharField(max_length=12, label="RUN")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

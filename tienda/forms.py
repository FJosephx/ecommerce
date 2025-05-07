from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CheckoutForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre de quien recibe',
        max_length=100,
        required=True
    )
    direccion = forms.CharField(
        label='Dirección',
        widget=forms.Textarea(attrs={'rows': 2}),
        required=True
    )
    numero_extra = forms.CharField(
        label='N° dpto, block o casa (opcional)',
        max_length=50,
        required=False
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=True
    )

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') 
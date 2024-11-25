from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import pycountry

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 'email', 'phone_number', 'wallet_address', 'country' ,'password1', 'password2'
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'first_name', 'last_name', 'email', 'wallet_address', 'country']
        widgets = {
            'country': forms.Select(choices=[(country.alpha_2, country.name) for country in pycountry.countries])
        }
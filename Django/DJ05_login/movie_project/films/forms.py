from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import Movie

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'review']  # укажи актуальные поля модели Movie
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Breeder

class BreederCreationForm(UserCreationForm):
    class Meta:
        model = Breeder
        fields = ('nickname', 'username')

from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Registration(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username','email','password1','password2']

class pets(forms.ModelForm):
  class Meta:
    model = Pets  
    fields = ['name','description','image','price']
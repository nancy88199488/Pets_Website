from PetParadise.forms import Registration
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def register(request):
  if request.method == 'POST':
    form = Registration(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data['email']
      username = form.cleaned_data.get('username')

      messages.success(request,f'Account for {username} created,you can now login')
      return redirect('login')
  else:
    form = Registration()
  return render(request,'registration/register.html',{"form":form}) 










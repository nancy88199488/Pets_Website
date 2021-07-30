from PetParadise.forms import Registration
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import render, redirect,get_object_or_404
import datetime as dt
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from .models import Pets,OrderPets, UserProfile,Order

# Create your views here.

def pets(request):
    context = {
        'pets': Pets.objects.all()
    }
    return render(request, "pets.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class HomeView(ListView):
    model = Pets
    paginate_by = 10
    template_name = "home.html"

class PetDetailView(DetailView):
    model = Pets
    template_name = "pets.html" 



@login_required
def add_to_cart(request, slug):
    pets = get_object_or_404(Pets, slug=slug)
    order_pets, created = OrderPets.objects.get_or_create(
        pets = pets,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.pets.filter(item__slug=pets.slug).exists():
            order_pets.quantity += 1
            order_pets.save()
            messages.info(request, "This pet types was updated.")
            return redirect("PetParadise:order-summary")
        else:
            order.pets.add(order_pets)
            messages.info(request, "This Pet was added to your cart.")
            return redirect("PetParadise:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.pets.add(order_pets)
        messages.info(request, "This pet was added to your cart.")
        return redirect("PetParadise:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Pets, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order pets is in the order
        if order.pets.filter(pets__slug=pets.slug).exists():
            order_pets = OrderPets.objects.filter(
                pets = pets,
                user=request.user,
                ordered=False
            )[0]
            order.pets.remove(order_pets)
            order_pets.delete()
            messages.info(request, "This pet was removed from your cart.")
            return redirect("PetParadise:order-summary")
        else:
            messages.info(request, "This pet was not in your cart")
            return redirect("PetParadise:pets", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("PetParadise:pets", slug=slug)           

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










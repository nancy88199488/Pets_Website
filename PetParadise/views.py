from django.shortcuts import render

# Create your views here.
def pet(request):
    context = {}
    return render(request,'pet/pet.html', context)

def checkout(request):
    context = {}
    return render(request,'pet/checkout.html', context)

def cart(request):
    context = {}
    return render(request,'pet/cart.html', context)        
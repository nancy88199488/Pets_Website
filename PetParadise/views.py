from django.shortcuts import render

# Create your views here.
def pet(request):
    context = {}
    return render(request,'pet/pet.html', context)
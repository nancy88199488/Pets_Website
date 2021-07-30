from django.contrib import admin
from .models import Pets,UserProfile,OrderPets


# Register your models here.
admin.site.register(Pets)
admin.site.register(UserProfile)
admin.site.register(OrderPets)
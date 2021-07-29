from django.urls import path
from . import views 
from .views import (PetDetailView,HomeView,add_to_cart,remove_from_cart)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('',views.index, name='index'),
    path('', HomeView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    # path('account/', include('django.contrib.auth.urls')),
    path('pets/<slug>/', PetDetailView.as_view(), name='pets'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),


    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
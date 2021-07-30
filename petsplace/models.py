from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.db.models import Sum
from cloudinary.models import CloudinaryField

# Create your models here.

class Pets(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PetParadise:pets", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("PetParadise:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("PetParadise:remove-from-cart", kwargs={
            'slug': self.slug
        })

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class OrderPets(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    pets = models.ForeignKey(Pets, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pets} of {self.pets.name}"

    def get_total_pets_price(self):
        return self.pets * self.pets.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    pets = models.ManyToManyField(OrderPets)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    '''
    1. Item added to cart
    
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_pets in self.pets.all():
            total += order_pets.get_final_price()

        return total        
    
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
    

from django import template
from PetParadise.models import Order

register = template.Library()


@register.filter
def cart_pets_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].pets.count()
    return 0
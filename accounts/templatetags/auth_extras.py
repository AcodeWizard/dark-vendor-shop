from django import template
from accounts.models import User
register = template.Library()

@register.filter(name='is_vendor')
def is_vendor(user):
    vendor=User.objects.filter(id=user.id,vendor=True).exists()
    return vendor
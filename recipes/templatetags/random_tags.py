from django import template
import random

register = template.Library()

@register.filter
def random_number(value):
    return random.randint(1, 2)
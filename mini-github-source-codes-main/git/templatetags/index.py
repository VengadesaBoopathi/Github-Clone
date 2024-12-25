from atexit import register
from django import template
import math
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def get_percentage(total, value):
    return (value/total)*80

@register.filter
def get_exact_percentage(total, value):
    return round((value/total)*100,2)
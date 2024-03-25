from django import template
from invclc.models import ModifiedInvoice

register = template.Library()

@register.filter
def convert_medical(value):
    words = value.split()
    if len(words) == 2:
        return ''.join(word[0] for word in words).upper()
    elif len(words) == 3:
        return ''.join(word[0] for word in words).upper()
    elif len(words) > 3:
        return ''.join(word[0] for word in words[:3]).upper()
    elif len(words) == 1:
        return words[0][0].upper()
    else:
        return "####"

from django import template

register = template.Library()

@register.filter
def convert_medical(value):
    words = value.split()
    if len(words) == 2:
        return '0' + ''.join(word[0] for word in words).upper()
    elif len(words) == 3:
        return ''.join(word[0] for word in words).upper()
    elif len(words) > 3:
        return ''.join(word[0] for word in words[:3]).upper()
    elif len(words) == 1:
        return '00' + words[0][0].upper()
    else:
        return "####"

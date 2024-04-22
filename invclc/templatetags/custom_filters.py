from django import template
from invclc.models import ModifiedInvoice
from authentication.models import CustomUser,Person
from django.core.exceptions import ObjectDoesNotExist

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

@register.filter
def medical_signup(medicals):
    try:
        medical_exists = Person.objects.filter(MedicalShopName=medicals).exists()
        person = Person.objects.get(MedicalShopName=medicals)
        user = person.user.username
        person_check = CustomUser.objects.filter(username=user).exists()

        if medical_exists:
            return "green"
        else:
            return "yellow"
        
    except Person.DoesNotExist:
        return "red"



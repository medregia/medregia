from django import template
from invclc.models import ModifiedInvoice
from authentication.models import CustomUser,Person
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from authentication.models import ConnectMedicals,Notification

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
def medical_signup(medicals,user):
    try:
        medical_exists = Person.objects.filter(MedicalShopName=medicals).exists()
        person = Person.objects.get(MedicalShopName=medicals)
        userId = person.UniqueId

        if "#" not in userId:
            return "green"
        else:
            return "red"

    except Person.DoesNotExist:
        return "red"



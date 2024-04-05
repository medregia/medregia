from django import template
from invclc.models import ModifiedInvoice
from authentication.models import CustomUser,Person

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


def check_medicals(medicals):
    # Logic to check if value exists in the database
    medical_exists = Person.objects.filter(MedicalShopName=medicals).exists()
    
    if medical_exists:
        try:
            get_medical = Person.objects.get(MedicalShopName=medicals)
            check_medicals = True  # or your logic to determine if value exists
        except Person.DoesNotExist:
            check_medicals = False
    else:
        check_medicals = False
    
    return {'check_medicals': check_medicals}

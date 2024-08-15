from django import template
from authentication.models import Person

register = template.Library()

@register.filter
def convert_medical(dl_number1="", dl_number2=""):
    words = []  # Initialize words to an empty list

    try:
        # Fetch the pharmacy name based on dl_number1 and dl_number2
        person = Person.objects.get(DrugLiceneseNumber1=dl_number1, DrugLiceneseNumber2=dl_number2)
        pharmacy_name = person.MedicalShopName
        words = pharmacy_name.split()

        # Use the pharmacy_name to get the medical username
        invoice_medical = person.user.username or ""
    except Person.DoesNotExist:
        invoice_medical = ""
    except Exception as e:
        print("In Convert Medicals:", e)
        invoice_medical = ""

    # Generate the final value based on the number of words
    if len(words) >= 3:
        return ''.join(word[0] for word in words[:3]).upper() + " - " + invoice_medical 
    elif len(words) == 2:
        return ''.join(word[0] for word in words).upper() + " - " + invoice_medical 
    elif len(words) == 1:
        return words[0][0].upper() + invoice_medical
    else:
        return "####"



@register.filter
def medical_signup(dl_number1, dl_number2):
    try:
        medical_exists = Person.objects.get(DrugLiceneseNumber1=dl_number1, DrugLiceneseNumber2=dl_number2)
        if not medical_exists:
            return "red"

        userId = medical_exists.UniqueId

        # Check if userId is not None and contains "#"
        if userId and "#" not in userId:
            return "green"
        else:
            return "orange"

    except Person.DoesNotExist:
        return "red"


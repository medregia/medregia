from django import forms
from .models import StateModel, DistrictModel, Person,Notification

class ProfileForm(forms.ModelForm):
    MedicalShopName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Medical Shop Name'}))
    ProprietaryName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Proprietary Name'}))
    ProprietaryNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Proprietary Number'}))
    ProprietaryContact = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Proprietary Contact'}))
    DrugLiceneseNumber1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Drug License Number 1'}))
    DrugLiceneseNumber2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Drug License Number 2'}))
    state = forms.ModelChoiceField(queryset=StateModel.objects.all())
    district = forms.ModelChoiceField(queryset=DistrictModel.objects.all())
    City = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))
    Pincode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pincode'}))
    StreetNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street Name'}), required=False)
    DoorNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Door Number'}), required=False)
    PharmacistName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pharmacist Name'}))
    RegisteredNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Registered Number'}))
    ContactNumber = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Contact Number'}))
    UniqueId = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Unique ID'}), required=False)

    class Meta:
        model = Person
        fields = ['MedicalShopName', 'ProprietaryName', 'ProprietaryNumber', 'ProprietaryContact', 'DrugLiceneseNumber1', 'DrugLiceneseNumber2', 'state', 'district', 'City', 'Pincode', 'StreetNumber', 'DoorNumber', 'PharmacistName', 'RegisteredNumber', 'ContactNumber', 'UniqueId']

            
class Notification(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter User Name Want to Admin '}))
    class Meta:
        model = Notification
        fields = [
            'message',
        ]
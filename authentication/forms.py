from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.core.validators import MaxValueValidator

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Enter Your Username','autocomplete':'off'}))
    phone_num = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter your phone number'}))
    pin = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your pin'}),
        validators=[MaxValueValidator(9999)]
    )
    STORE_TYPES = [
        ('', 'Select'),
        ('retailer', 'Retailer'),
        ('manufacturer', 'Manufacturer'),
        ('pharmacy', 'Pharmacy'),
        ('medical', 'Medical'),
        ('others', 'Others'),
    ]
    store_type = forms.ChoiceField(choices=STORE_TYPES)
    other_value = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'Categories'}), required=False)

    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email','value':'@gmail.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email', 'password1', 'password2', 'phone_num', 'pin', 'store_type', 'other_value',
        )
        

class InsensitiveAuthentication(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username__iexact=username)
                if user.username == username:
                    return username
            except CustomUser.DoesNotExist:
                pass
        raise forms.ValidationError("Invalid username is not Valid")

        
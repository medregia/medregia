from django import forms
from .models import Invoice
from django.utils import timezone
from datetime import timedelta

class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        
        # Set default value for invoice_date
        # self.fields['invoice_date'].initial = timezone.now().date()
        
        # Calculate current time and add 5 hours and 31 minutes
        current_time = timezone.now() + timedelta(hours=5, minutes=31)
        self.fields['current_time'].initial = current_time.time()

    invoice_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY', 'title': 'Default today Date'})
    )

    class Meta:
        model = Invoice
        fields = ['pharmacy_name', 'invoice_number', 'invoice_date', 'invoice_amount', 'balance_amount', 'payment_amount', 'today_date', 'current_time', 'updated_by']
        widgets = {
            'pharmacy_name': forms.TextInput(attrs={'placeholder': 'Pharmacy Name','class':'pharmacy_name'}),
            'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number','value':'IV-','class':'invoice_number'}),
            'invoice_amount': forms.NumberInput(attrs={'placeholder': 'Invoice Amount','class':'invoice_amount'}),
            'balance_amount': forms.TextInput(attrs={'placeholder': 'Balance Amount', 'disabled': True,'class':'balance_amount'}),
            'payment_amount': forms.NumberInput(attrs={'placeholder': '0','title':'Default 0 ','class':'payment_amount'}),
            'today_date':forms.DateInput(attrs={'type':'hidden'}),
            'current_time':forms.TimeInput(attrs={'type':'hidden'}),
            'updated_by':forms.TextInput(attrs={'type':'hidden',}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
        })
    )
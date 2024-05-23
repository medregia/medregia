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
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'})
    )
    
    def clean_invoice_date(self):
        invoice_date = self.cleaned_data.get("invoice_date")
        if not invoice_date:
            raise forms.ValidationError("Invoice date format is not valid.")
        return invoice_date

    def clean(self):
        cleaned_data = super().clean()
        invoice_amount = cleaned_data.get("invoice_amount")
        payment_amount = cleaned_data.get("payment_amount")

        if payment_amount is not None and invoice_amount is not None:
            if payment_amount > invoice_amount:
                raise forms.ValidationError({"payment_amount":"The payment amount not Valid."})
        
        return cleaned_data
    
    def clean_invoice_number(self):
        invoice_number = self.cleaned_data.get("invoice_number")
        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            raise forms.ValidationError("Invoice number must be unique.")
        return invoice_number

    class Meta:
        model = Invoice
        fields = ['pharmacy_name', 'invoice_number', 'invoice_date', 'invoice_amount', 'balance_amount', 'payment_amount', 'today_date', 'current_time', 'updated_by']
        widgets = {
            'pharmacy_name': forms.TextInput(attrs={'placeholder': 'Pharmacy Name','class':'pharmacy_name'}),
            'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number','class':'invoice_number'}),
            'invoice_amount': forms.NumberInput(attrs={'placeholder': 'Invoice Amount','class':'invoice_amount'}),
            'balance_amount': forms.TextInput(attrs={'placeholder': 'Balance Amount', 'disabled': True,'class':'balance_amount'}),
            'payment_amount': forms.NumberInput(attrs={'placeholder': '0','title':'Default 0 ','class':'payment_amount','default':'0'}),
            'today_date':forms.DateInput(attrs={'type':'hidden'}),
            'current_time':forms.TimeInput(attrs={'type':'hidden'}),
            'updated_by':forms.TextInput(attrs={'type':'hidden',}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        widget=forms.FileInput(attrs={
            'accept': '.csv',
            'class':'csv-field',
            'id':'fileInput',
        })
    )   
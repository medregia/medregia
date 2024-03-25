from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    invoice_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY', 'title': 'Default today Date'})
    )

    class Meta:
        model = Invoice
        fields = ['pharmacy_name', 'invoice_number', 'invoice_date', 'invoice_amount', 'balance_amount', 'payment_amount','today_date']
        widgets = {
            'pharmacy_name': forms.TextInput(attrs={'placeholder': 'Pharmacy Name','class':'pharmacy_name'}),
            'invoice_number': forms.TextInput(attrs={'placeholder': 'Invoice Number','value':'IV-','class':'invoice_number'}),
            'invoice_amount': forms.NumberInput(attrs={'placeholder': 'Invoice Amount','class':'invoice_amount'}),
            'balance_amount': forms.TextInput(attrs={'placeholder': 'Balance Amount', 'disabled': True,'class':'balance_amount'}),
            'payment_amount': forms.NumberInput(attrs={'placeholder': '0','title':'Default 0 ','class':'payment_amount'}),
            'today_date':forms.DateInput(attrs={'type':'hidden'}),
            'current_time':forms.TimeInput(attrs={'type':'hidden'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.csv', '.json')):
            raise forms.ValidationError("File format not supported. Please upload a CSV or JSON file.")
        return file
from django import forms
from .models import Invoice
from django.utils import timezone
from datetime import timedelta

class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        
        # Set default value for invoice_date
        self.fields['invoice_date'].initial = timezone.now().date()
        
        # Calculate current time and add 5 hours and 31 minutes
        current_time = timezone.now() + timedelta(hours=5, minutes=31)
        self.fields['current_time'].initial = current_time.time()

    invoice_date = forms.DateField(
        input_formats=['%d/%m/%Y', '%d-%m-%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY', 'title': 'Default today Date'})
    )

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.csv', '.json')):
            raise forms.ValidationError("File format not supported. Please upload a CSV or JSON file.")
        return file
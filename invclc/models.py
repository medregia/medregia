from django.db import models
from django.utils import timezone
from authentication.models import CustomUser
from simple_history.models import HistoricalRecords

class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    pharmacy_name = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=20, unique=True)
    invoice_date = models.DateField(default=timezone.now)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    today_date = models.DateField(default=timezone.now)
    history = HistoricalRecords() 

    def save(self, *args, **kwargs):
        self.balance_amount = self.invoice_amount - self.payment_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.pharmacy_name}"
    
class DeletedInvoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    pharmacy = models.CharField(max_length=100)
    number = models.CharField(max_length=20, unique=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    today_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.pharmacy}-{self.today_date}"
    
class ModifiedInvoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    modified_pharmacy = models.CharField(max_length=100)
    modified_Invoice_number = models.CharField(max_length=20, unique=True)
    modified_Invoice_date = models.DateField(default=timezone.now)
    modified_Total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    modified_balance = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    modified_payment = models.DecimalField(max_digits=10, decimal_places=2)
    modified_today_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.modified_pharmacy}-{self.modified_today_date}"
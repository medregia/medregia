from django.db import models
from django.utils import timezone
from authentication.models import CustomUser
from simple_history.models import HistoricalRecords
from datetime import timedelta
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver

class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    pharmacy_name     = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(default=timezone.now)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    today_date = models.DateField(default=timezone.now)
    # current_time = models.TimeField(default=(timezone.now() + timedelta(hours=5, minutes=30)).time())
    current_time = models.TimeField(default=timezone.now)
    updated_by = models.CharField(max_length=20,null=True,blank=True)

    def save(self, *args, **kwargs):
        self.balance_amount = self.invoice_amount - self.payment_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.pharmacy_name}"

    
class DeletedInvoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    pharmacy = models.CharField(max_length=100)
    number = models.CharField(max_length=50, unique=True)
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
    modified_Invoice_number = models.CharField(max_length=50, unique=True)
    modified_Invoice_date = models.DateField(default=timezone.now)
    modified_Total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    modified_balance = models.DecimalField(max_digits=10, decimal_places=2 ,null=True, blank=True)
    modified_payment = models.DecimalField(max_digits=10, decimal_places=2)
    modified_today_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        
        return f"{self.modified_pharmacy}-{self.modified_today_date}"
    
class TrackingPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    Medical_name = models.CharField(max_length = 100)
    Medical_payments = models.DecimalField(max_digits=20, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    paying_amount = models.DecimalField(max_digits = 20 ,decimal_places=2, null=True)
    
    def __str__(self):
        return f"{self.user} - {self.Medical_payments} - {self.payment_date}"
    

@receiver(pre_delete, sender=Invoice)
def delete_tracking_payments(sender, instance, **kwargs):
    TrackingPayment.objects.filter(Medical_name=instance.pharmacy_name).delete()
    
@receiver(pre_save, sender=Invoice)
def update_tracking_payments(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Invoice.objects.get(pk=instance.pk)
        # Check if the pharmacy_name has been modified
        if instance.pharmacy_name != original_instance.pharmacy_name:
            # Update the corresponding Medical_name in TrackingPayment
            TrackingPayment.objects.filter(Medical_name=original_instance.pharmacy_name, user=instance.user).update(Medical_name=instance.pharmacy_name)
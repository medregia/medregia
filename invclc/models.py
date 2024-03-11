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

    def _str_(self):
        return f"{self.pharmacy_name} - {self.invoice_number}"
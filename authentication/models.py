# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError

class StateModel(models.Model):
    Pid = models.IntegerField(primary_key=True)
    LocationType = models.CharField(max_length=100)
    Pname = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Pname
   
class DistrictModel(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE,null=True)
    Pid = models.IntegerField()
    LocationType = models.CharField(max_length=100)
    districtname = models.CharField(max_length=100)
    
    def __str__(self):
        return self.districtname
        
class CustomUser(AbstractUser):
    STORE_TYPES = [
        ('retailer', 'Retailer'),
        ('manufacturer', 'Manufacturer'),
        ('pharmacy', 'Pharmacy'),
        ('medical', 'Medical'),
        ('others', 'Others'),
    ]

    POSITION_CHOICES = [
        ('Admin', 'Admin'),
        ('Senior', 'Senior'),
        ('Member', 'Member'),
        ('NewUser', 'NewUser')
    ]

    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    phone_num = models.CharField(max_length=15, blank=True, verbose_name='Phone Number')
    email = models.EmailField(unique=True, verbose_name='Email')
    pin = models.PositiveIntegerField(blank=True, null=True, verbose_name='PIN')
    
    store_type = models.CharField(max_length=50, choices=STORE_TYPES, null=True, blank=True, verbose_name='Store Type')
    other_value = models.CharField(max_length=50, null=True, blank=True, verbose_name='Other Value')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, null=True, blank=True, default="Admin", verbose_name='Position')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='Groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='User Permissions',
        help_text='Specific permissions for this user.',
    )
    
    # class Meta:
    #     permissions = [
    #         ("view_own_details", "Can view own details"),
    #     ]
    
    def __str__(self):
        return self.username
    
class Person(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    MedicalShopName = models.CharField(max_length=100, blank=True, null=True)
    ProprietaryName = models.CharField(max_length=100, blank=True, null=True)
    ProprietaryNumber = models.CharField(max_length=100, blank=True, null=True)
    ProprietaryContact = models.CharField(max_length=100, blank=True, null=True)
    DrugLiceneseNumber2 = models.CharField(max_length=100, blank=True, null=True)
    DrugLiceneseNumber1 = models.CharField(max_length=100, blank=True, null=True)

    # Registered Address
    state = models.ForeignKey(StateModel, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True, blank=True)
    City = models.CharField(max_length=100, blank=True, null=True)
    Pincode = models.CharField(max_length=100, blank=True, null=True)
    StreetNumber = models.CharField(max_length=100, blank=True, null=True)
    DoorNumber = models.CharField(max_length=100, blank=True, null=True)

    PharmacistName = models.CharField(max_length=100, blank=True, null=True)
    RegisteredNumber = models.CharField(max_length=100, blank=True, null=True)
    ContactNumber = models.CharField(max_length=15, blank=True, null=True)
    PharmacistEmail = models.EmailField(blank = True,null=True)

    UniqueId = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        MedicalShopName = self.MedicalShopName or ''
        return MedicalShopName
    
class Notification(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    request_status = models.BooleanField(default = True)
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"Notification from {self.sender.username} to {self.receiver.username}"
    
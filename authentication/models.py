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
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE,null=True)
    Pid = models.IntegerField()
    LocationType = models.CharField(max_length=100)
    districtname = models.CharField(max_length=100)
    
    def __str__(self):
        return self.districtname

        
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    phone_num = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    pin = models.IntegerField(blank=True ,null=True)
    
    STORE_TYPES = [
        ('retailer', 'Retailer'),
        ('manufacturer', 'Manufacturer'),
        ('pharmacy', 'Pharmacy'),
        ('medical', 'Medical'),
        ('others', 'Others'),
    ]
    store_type = models.CharField(max_length=50, choices=STORE_TYPES,null=True,blank=True)
    other_value = models.CharField(max_length=50 ,null=True,blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    # class Meta:
    #     permissions = [
    #         ("view_own_details", "Can view own details"),
    #     ]
    
    def _str_(self):
        return self.username
    
class Person(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    MedicalShopName = models.CharField(max_length=100, blank=True, null=True,)
    ProprietaryName = models.CharField(max_length=100, blank=True, null=True,)
    ProprietaryNumber = models.CharField(max_length=100, blank=True, null=True,)
    ProprietaryContact = models.CharField(max_length=100, blank=True, null=True)
    DrugLiceneseNumber2 = models.CharField(max_length=100, blank=True, null=True,)
    DrugLiceneseNumber1 = models.CharField(max_length=100, blank=True, null=True,)

    # Registered Address
    state = models.ForeignKey(StateModel, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True, blank=True)
    City = models.CharField(max_length=100, blank=True, null=True)
    Pincode = models.CharField(max_length=100, blank=True, null=True)
    StreetNumber = models.CharField(max_length=100, blank=True, null=True)
    DoorNumber = models.CharField(max_length=100, blank=True, null=True)

    PharmacistName = models.CharField(max_length=100, blank=True, null=True)
    RegisteredNumber = models.CharField(max_length=100, blank=True, null=True,)
    ContactNumber = models.CharField(max_length=15, blank=True, null=True)

    UniqueId = models.CharField(max_length=100, blank=True, null=True,)

    def __str__(self):
        return self.MedicalShopName
    
    def clean(self):
        # Check if DrugLiceneseNumber1 is not empty or None
        if self.DrugLiceneseNumber1:
            # Check if there is any other Person object with the same DrugLiceneseNumber1
            if Person.objects.exclude(pk=self.pk).filter(DrugLiceneseNumber1=self.DrugLiceneseNumber1).exists():
                raise ValidationError({'DrugLiceneseNumber1': 'DrugLiceneseNumber1 has already recorded'})

        if self.ProprietaryName:
            # Check if there is any other Person object with the same ProprietaryName
            if Person.objects.exclude(pk=self.pk).filter(ProprietaryName=self.ProprietaryName).exists():
                raise ValidationError({'ProprietaryName': 'ProprietaryName has already recorded'})
            
        if self.ProprietaryNumber:
            # Check if there is any other Person object with the same ProprietaryName
            if Person.objects.exclude(pk=self.pk).filter(ProprietaryNumber=self.ProprietaryNumber).exists():
                raise ValidationError({'ProprietaryNumber': 'ProprietaryNumber has already recorded'})
            
        if self.ProprietaryContact:
            # Check if there is any other Person object with the same ProprietaryName
            if Person.objects.exclude(pk=self.pk).filter(ProprietaryContact=self.ProprietaryContact).exists():
                raise ValidationError({'ProprietaryContact': 'ProprietaryContact has already recorded'})
            
        if self.DrugLiceneseNumber2:
            # Check if there is any other Person object with the same ProprietaryName
            if Person.objects.exclude(pk=self.pk).filter(DrugLiceneseNumber2=self.DrugLiceneseNumber2).exists():
                raise ValidationError({'DrugLiceneseNumber2': 'DrugLiceneseNumber2 has already recorded'})
            
        if self.RegisteredNumber:
            # Check if there is any other Person object with the same ProprietaryName
            if Person.objects.exclude(pk=self.pk).filter(RegisteredNumber=self.RegisteredNumber).exists():
                raise ValidationError({'RegisteredNumber': 'RegisteredNumber has already recorded'})
    
class Notification(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=True)
    request_status = models.BooleanField(default = True)
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"Notification from {self.sender.username} to {self.receiver.username}"
    
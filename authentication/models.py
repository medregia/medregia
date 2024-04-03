# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Permission
from django.core.validators import RegexValidator

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
    username_validator = RegexValidator(r'^[a-zA-Z\-_]+\Z', 'Only letters, hyphens, and underscores are allowed.')

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )

    def authenticate(self, **kwargs):
        username = kwargs['username'].lower()
        password = kwargs['password']
        try:
            user = self.get(username=username)
        except self.DoesNotExist:
            # If the user does not exist, create a new user with the lowercase username
            # and password
            user = self.create(username=username, password=password)
            user.save()
        else:
            # If the user exists, make sure the user has the correct password
            if not user.check_password(password):
                return None
        # If the user exists and has the correct password, save the lowercase username
        # to the database
        user.username = user.username.lower()
        user.save()
        return user
        
    phone_num = models.CharField(max_length=15, blank=False)
    email = models.EmailField(unique=True)
    pin = models.IntegerField(blank=False ,null=True)
    
    STORE_TYPES = [
        ('retailer', 'Retailer'),
        ('manufacturer', 'Manufacturer'),
        ('pharmacy', 'Pharmacy'),
        ('medical', 'Medical'),
        ('user','User'),
        ('others', 'Others'),
    ]
    store_type = models.CharField(max_length=50, choices=STORE_TYPES,null=False,blank=False)
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
    
    def __str__(self):
        return self.username 
    
class Person(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True)
    MedicalShopName = models.CharField(max_length=100 ,blank=False,null=False)
    ProprietaryName = models.CharField(max_length=100 ,blank=False,null=False)
    ProprietaryNumber = models.CharField(max_length=100 ,blank=False,null=False)
    ProprietaryContact = models.CharField(max_length=100 ,blank=False,null=False)
    DrugLiceneseNumber1 = models.CharField(max_length=100 ,blank=False,null=False)
    DrugLiceneseNumber2 = models.CharField(max_length=100 ,blank=False,null=False)

    #Registered Address
    state = models.ForeignKey(StateModel, on_delete=models.SET_NULL, null=True,blank=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True,blank=True)
    City = models.CharField(max_length=100 ,blank=False,null=False)
    Pincode = models.CharField(max_length=100 ,blank=False,null=False)
    StreetNumber = models.CharField(max_length=100 ,blank=True,null=True)
    DoorNumber = models.CharField(max_length=100 ,blank=True,null=True)
    
    PharmacistName =  models.CharField(max_length=100 ,blank=False,null=False)
    RegisteredNumber =  models.CharField(max_length=100 ,blank=False,null=False)
    ContactNumber =  models.CharField( max_length = 15, blank=False,null=False)
    UniqueId = models.CharField(max_length=100 ,blank=True,null=True)    
    
    def __str__(self):
        return self.name
    
    
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
    
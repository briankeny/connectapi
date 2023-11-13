from django.db import models
from .managers import UserManager
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User(AbstractUser, PermissionsMixin):
    accounts = (
        ('personal', 'personal'),
        ('organization', 'organization'),
    )
    employment_types = (
        ('permanent', 'permanent'),
        ('temporary', 'temporary'),
        ('contract', 'contract')    
    )
    genders = (
        ('male', 'male'),
        ('female', 'female'),
        ('n/a', 'N/A')    
    )
    username = models.CharField(max_length=20,primary_key=True,default=None)
    bio = models.CharField(max_length=30, default=None, null=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    account_type = models.CharField(  
        max_length=30,
        choices=accounts,
        default='personal')
    mobile_number = models.CharField(max_length=30, default=None, null=True,blank=True)
    date_of_birth = models.DateField( default=None, null=True,blank=True)
    password = models.CharField(max_length=100, null=False,default=None)
    gender = models.CharField(  
        max_length=30,
        choices=genders,
        default='n/a')
    
    date_updated = models.DateTimeField(default=timezone.now)
   
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"   
    
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

    REQUIRED_FIELDS = ['first_name','last_name','email','account_type']
  

    def __str__(self):
        return f'{self.username}{self.first_name}'



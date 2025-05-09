from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .myusermanager import Usermanager
from shortuuid.django_fields import ShortUUIDField




class MyUser (AbstractBaseUser):
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='abcdefghijklmnqszxcvopl1234567890')
    phone = models.CharField(unique=True, max_length=100)
    email  = models.CharField(max_length=30)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=40)
    last_name =  models.CharField(max_length=50)
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)# a admin user; non super-user
    is_admin =  models.BooleanField(default=False) # a superuser
    is_facilitator = models.BooleanField(default=False)
    is_verified_facilitator = models.BooleanField(default=False)
     
    def __str__(self):
        return self.username
    objects = Usermanager()
    
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    
    
    
    def get_full_name(self):
        return self.first_name
            # The full name is identified by their email address
    
    def get_short_name(self):
        return self.email
        # The full name is identified by their email address
        
        
    
    def has_perm(self,perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
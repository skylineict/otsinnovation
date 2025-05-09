from django.db import models
from django.contrib.auth import get_user_model
from dash.models import Cohorts
from shortuuid.django_fields import ShortUUIDField


User =  get_user_model()









class Profiles(models.Model):
    adminsion_status = (
    ('pending', 'pending'),
    ('rejected', 'rejected'),
    ('admitted', 'admitted')
    )
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='abcdefghijklmnqszxcvopl1234567890')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    state =    models.CharField(max_length=200)
    city  =    models.CharField(max_length=200)
    local_govt = models.CharField(max_length=200)
    phone_num =  models.CharField(max_length=200)
    contact_add = models.CharField(max_length=600)
    laptop  =   models.CharField(max_length=200)
    certifcate  = models.CharField(max_length=200)
    occupation   =  models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status =   models.CharField(max_length=50, choices=adminsion_status, default='pending')
    uplaod_picture =  models.ImageField(upload_to='profile', default=2)
    sponsorship = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateField(auto_now=True, auto_now_add=True)
    created = models.DateField(auto_now=True)
    
    
   
    


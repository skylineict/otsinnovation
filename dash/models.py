from django.db import models
from django.contrib.auth import get_user_model
import random
import string
User = get_user_model()
# Create your models here.

class Cohorts(models.Model):
    name = models.CharField(max_length=200, unique=True)
    users  = models.ManyToManyField(User)
    whatsapp = models.CharField(max_length=400, blank=True, null=True, default='hello')
    
    
    def __str__(self):
        return self.name



class Payment(models.Model):
    payment = (
    ('pending', "pending"),
    ('approved', "approved"),
    ('reject', "reject"),
    )
    amount = models.IntegerField()
    courses = models.CharField(max_length=200) 
    payment_type = models.CharField(max_length=200)
    date =      models.DateField(auto_now_add=True)
    uplaod     =   models.ImageField(upload_to='payment')
    user   =     models.ForeignKey(User, on_delete=models.CASCADE)
    passcode =    models.CharField(max_length=20)
    payment_status = models.CharField(max_length=200,choices=payment, default='pending')
    
    def __str__(self):
        return  str(self.user)
    
    def total_amount(user):
        my_amount = Payment.objects.filter(user=user)
        my_total_amount = sum(amounts.amount for amounts in my_amount)
        return my_total_amount
        
    
    def mysave(self, *args, **kwargs):
        mycode = "PASS-"
        if self.payment_status == 'approved' and not self.passcode:
            self.passcode = mycode + "".join(random.choices(string.digits,k=5))
            
            
        super().save(*args, **kwargs)
        

class Mypasscode(models.Model):
    passcodeNo = models.CharField(max_length=200, unique=True) 
    student = models.ForeignKey(User,on_delete=models.CASCADE)   

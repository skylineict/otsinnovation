from django.contrib import admin
from .models import Cohorts,Payment, Mypasscode
from django.forms.widgets import CheckboxSelectMultiple
from django.db import models

# Register your models here.


@admin.register(Cohorts)
class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

        
# @admin.register(Cohorts)
# class Cohorts(admin.ModelAdmin):
#     # list_display = ('name', 'users')
#     pass

@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ('user','amount', 'courses')
    
@admin.register(Mypasscode)
class passcode(admin.ModelAdmin):
    list_display = ('passcodeNo', 'student')
   

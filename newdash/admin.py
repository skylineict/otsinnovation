from django.contrib import admin
from .models import FacilitatorRegistration

# Register your models here.



@admin.register(FacilitatorRegistration)
class FacilitatorReg(admin.ModelAdmin):
    list_display = ('id','user','course','approved','registration_date') 


    
     
    
      
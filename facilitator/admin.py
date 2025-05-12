from django.contrib import admin

# Register your models here.
from .models import FacilitatorRegistration


@admin.register(FacilitatorRegistration)
class FacilitatorReg(admin.ModelAdmin):
    list_display = ('id','user','course','approved','registration_date') 


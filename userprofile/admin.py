from django.contrib import admin
from .models import Profiles

# Register your models here.
@admin.register(Profiles)
class Profile(admin.ModelAdmin):
    list_display = ('id','first_name',  'last_name', 'state', 'phone_num', 'status')





from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

# User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','phone', 'email', 'is_admin', 'username')
    list_filter = ('is_admin',)
    
    
admin.site.register(MyUser, CustomUserAdmin)
    

   




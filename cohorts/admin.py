from django.contrib import admin
from .models import Livesesion,Trainingsession,Recapsesion,Recapcourse,Ourteam

# Register your models here.
@admin.register(Livesesion)
class Livesession(admin.ModelAdmin):
    list_display = ('title','subject','link','date','online','courses')
    
    
@admin.register(Trainingsession)
class traininsession(admin.ModelAdmin):
    list_display = ('name',)

    
@admin.register(Recapsesion)
class Recap(admin.ModelAdmin):
    list_display = ('title','date', 'link')
    
    
@admin.register(Recapcourse)
class Recap(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Ourteam)
class Ourteam(admin.ModelAdmin):
    list_display = ('name','files','link')

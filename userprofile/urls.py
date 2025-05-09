from django.contrib import admin
from django.urls import path
from .views import Profile

urlpatterns = [
    
    path('', Profile.as_view(), name='profile'),
    
    
    
    
]

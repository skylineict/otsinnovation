from django.urls import path
from .views import Messages





urlpatterns = [
    
    path('', Messages.as_view(), name='send_email')
   
    
    
]


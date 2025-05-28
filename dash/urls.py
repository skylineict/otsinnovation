from django.urls import path
from .views import   Dashboard



urlpatterns = [
    path('', Dashboard.as_view(), name='dash'),
    
 
   
   
    # path('passcode', Passcode.as_view(), name='passcode')
    
]

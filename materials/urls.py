from django.urls import path
from .views import html5,css5




urlpatterns = [
    path('pdf',html5, name='htmlpdf'),
    path('css',css5, name='csspdf'),
    path('product',css5, name='product')
   
   
    # path('passcode', Passcode.as_view(), name='passcode')
    
]
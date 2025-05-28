from django.urls import path
from .liveclass import LiveclassVIeiw


urlpatterns = [
   path('', LiveclassVIeiw.as_view(), name="classroom"),

   
   
   
]

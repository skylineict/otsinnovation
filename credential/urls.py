from django.urls import path
from .views import Forgetphone,Myemail,payment_rejected,PasswordRest,Set_NewPassword,CompletePassword




urlpatterns = [
    path('', Forgetphone.as_view(), name="phone"),
    path('email', Myemail.as_view(), name="email"),
    path('reject_paymment',payment_rejected.as_view(), name='payment_reject'),
    path('password', PasswordRest.as_view(), name="password"),
    path('set_password/<uidb64>/<token>',Set_NewPassword.as_view(), name='mypassword'),
    path('complete', CompletePassword.as_view(), name="complete"),
    
   
]

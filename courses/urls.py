from django.urls import path
from . register_courses import CourseRegistrationView,fetch_all_courses
from .coursesinfo import  PaymentDetailView
from .webhook import flutterwave_webhook
from .verify_payment import verify_payment
from .bank import debug_banks



urlpatterns = [
 #this is the url for the course registration view
    path('', CourseRegistrationView.as_view(), name='register_course'),
    path('fetch_all_courses',fetch_all_courses, name='all_courses'),
    path('courseinfo/<str:registration_id>/',PaymentDetailView.as_view(), name='courseinfo'),
    #payment handler urls
    
    path('webhooks/flutterwave/', flutterwave_webhook, name='flutterwave_webhook'),
    path('verify_payment/<str:payment_id>/',verify_payment, name='verify_payment'),
    path('banks', debug_banks, name='debug_banks'),

    

]


# urlpatterns = [
#     path('payment/<str:registration_id>/', views.payment_form, name='payment_form'),
#     path('payment/processor/<str:payment_id>/<str:tx_ref>/', views.payment_processor, name='payment_processor'),
#     path('payment/callback/', views.payment_callback, name='payment_callback'),
#     path('payment/verify/<str:payment_id>/', views.verify_payment, name='verify_payment'),
# ]

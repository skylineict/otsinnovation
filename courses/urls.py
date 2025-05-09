from django.urls import path
from django.contrib import admin
from . register_courses import CourseRegistrationView,fetch_all_courses
from .coursesinfo import  PaymentDetailView



urlpatterns = [
 #this is the url for the course registration view
    path('', CourseRegistrationView.as_view(), name='register_course'),
    path('fetch_all_courses',fetch_all_courses, name='all_courses'),
    path('courseinfo/<slug:registration_id>/',PaymentDetailView.as_view(), name='courseinfo'),
    # path('courseinfofetch/<slug:registration_id>/',Courseinfetch.as_view(), name='courseinfofetch'),
    
]


# urlpatterns = [
#     path('payment/<str:registration_id>/', views.payment_form, name='payment_form'),
#     path('payment/processor/<str:payment_id>/<str:tx_ref>/', views.payment_processor, name='payment_processor'),
#     path('payment/callback/', views.payment_callback, name='payment_callback'),
#     path('payment/verify/<str:payment_id>/', views.verify_payment, name='verify_payment'),
# ]

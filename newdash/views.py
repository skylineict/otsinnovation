from django.views import View
from django.shortcuts import render
from courses.models import Course, CourseRegistration,  PaymentDetail, Transaction

def payment_success(request):
    return render(request, 'payment_success.html') 
 # -------------------------
# Flutterwave Webhook Handler
# -------------------------

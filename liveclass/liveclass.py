
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from courses.models import Course, CourseRegistration
from registration.models import MyUser




class LiveclassVIeiw(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        registration = CourseRegistration.objects.filter(user=request.user).first()
        if registration and registration.account_suspended:
            return redirect('dashboard')
       
        return render(request, 'dashboard/students/classroom.html')
        
    
    def post(self, request):
            
        registration = CourseRegistration.objects.filter(user=request.user).first()
        if registration and registration.account_suspended:
                 return redirect('dashboard')
        return render(request, 'dashboard/students/classroom.html')
    
    

    
     

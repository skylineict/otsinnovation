
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from courses.models import Course, CourseRegistration
from registration.models import MyUser

logger = logging.getLogger(__name__)

class AdminLiveclassView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        if not (request.user.is_facilitator or request.user.is_staff or request.user.is_admin):
            return redirect('dashboard')
       
        registration = CourseRegistration.objects.filter(user=request.user).first()
        if registration and registration.account_suspended:
            return redirect('dashboard')
        
        return render(request, 'admindash/facilitator/classroom.html')

    def post(self, request):
        if not (request.user.is_facilitator or request.user.is_staff or request.user.is_admin):
            return JsonResponse({'error': 'You do not have permission to perform this action'}, status=403)
        registration = CourseRegistration.objects.filter(user=request.user, is_approved=True).first()
        if registration and registration.account_suspended:
            return JsonResponse({'error': 'Your account is suspended'}, status=403)
        
from venv import logger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
import logging
from .models import FacilitatorRegistration
from courses.models import Course,CourseRegistration






class FacilitatorRegistrationView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # Check if user is suspended
        registration = CourseRegistration.objects.filter(user=request.user).first()
        if registration and registration.account_suspended:
           return JsonResponse({'error': 'Your account is suspended', 'redirect': 'dashboard'}, status=403)
          # Check if user has any facilitator registrations
        has_registration = FacilitatorRegistration.objects.filter(user=request.user).exists()
        
        
         # Get courses that do not have any approved facilitator registrations
        approved_courses = FacilitatorRegistration.objects.filter(approved=True).values_list('course_id', flat=True)
        courses = Course.objects.exclude(id__in=approved_courses)
        return render(request, 'facilitator/request_form.html', {'courses': courses, 'has_registration': has_registration}) 
    
    def post(self, request):
        # Check if user is suspended
        registration = CourseRegistration.objects.filter(user=request.user, is_approved=True).first()
        if registration and registration.account_suspended:
            return JsonResponse({'error': 'Your account is suspended'}, status=403)
        
        course_id = request.POST.get('course')
        linkedin = request.POST.get('linkedin', '')
        twitter = request.POST.get('twitter', '')
        github = request.POST.get('github', '')
        facebook = request.POST.get('facebook', '')

         # Validate required fields
        if not course_id:
            return JsonResponse({'error': 'Course ID is required'}, status=400)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Invalid course selected'}, status=400)
         # Check if user already applied for this course
        if FacilitatorRegistration.objects.filter(user=request.user, course=course).exists():
            return JsonResponse({'error': 'You have already applied to facilitate this course'}, status=400)
        
         # Check if the course already has an approved facilitator
        if FacilitatorRegistration.objects.filter(course=course, approved=True).exists():
            return JsonResponse({'error': 'This course already has an approved facilitator'}, status=400)

        # Check if user already applied for this course
        if FacilitatorRegistration.objects.filter(user=request.user, course=course).exists():
            return JsonResponse({'error': 'You have already applied to facilitate this course'}, status=400)
        try:
            facilitator_registration = FacilitatorRegistration.objects.create(
                    user=request.user,
                    course=course,
                    linkedin=linkedin,
                    twitter=twitter,
                    github=github,
                    facebook=facebook,  )
                   
                # Notify user
            send_mail(
                    subject="Facilitator Application Submitted",
                    message=f"Your application to facilitate {course.name} has been submitted and is pending approval.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
            
            return JsonResponse({
                    'success': f'Application for {course.name} submitted successfully'
                })
        except Exception as e:
            logger.error(f"Error submitting facilitator application: {e}")
            return JsonResponse({'error': 'Application submission failed'}, status=500)
        

    



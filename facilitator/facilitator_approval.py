
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from courses.models import Course, CourseRegistration
from registration.models import MyUser
from .models import FacilitatorRegistration
from django.contrib.auth import logout

logger = logging.getLogger(__name__)
class FacilitatorApprovalView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # Restrict to staff or admin users
        if not (request.user.is_staff or request.user.is_admin):
            logout(request) 
            return redirect('login') # Log out the user if they don't have permission
         
            
        
        # Check if user is suspended
        registration = CourseRegistration.objects.filter(user=request.user).first()
        if registration and registration.account_suspended:
            return render(request, 'admindash/facilitator/facilitator_approval.html', {'error': 'Your account is suspended'})
        
        # Get pending facilitator registrations
        pending_registrations = FacilitatorRegistration.objects.filter(approved=False)
        return render(request, 'admindash/facilitator/facilitator_approval.html', {
            'registrations': pending_registrations
        })

    def post(self, request):
        # Restrict to staff or admin users
        if not (request.user.is_staff or request.user.is_admin):
            return JsonResponse({'error': 'You do not have permission to perform this action'}, status=403)
        
        # Check if user is suspended
        registration = CourseRegistration.objects.filter(user=request.user, is_approved=True).first()
        if registration and registration.account_suspended:
            return JsonResponse({'error': 'Your account is suspended'}, status=403)

        # Get form data
        registration_id = request.POST.get('registration_id')
        action = request.POST.get('action')  # 'approve' or 'reject'

        # Validate required fields
        if not registration_id or not action:
            return JsonResponse({'error': 'Registration ID and action are required'}, status=400)

        if action not in ['approve', 'reject']:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        try:
            facilitator_registration = FacilitatorRegistration.objects.get(id=registration_id)
        except FacilitatorRegistration.DoesNotExist:
            return JsonResponse({'error': 'Invalid registration ID'}, status=400)

        try:
            with transaction.atomic():  # Ensure all database operations are atomic
                if action == 'approve':
                    # Check if another approved facilitator exists for the course
                    if FacilitatorRegistration.objects.filter(course=facilitator_registration.course, approved=True).exists():
                        return JsonResponse({
                            'error': f'Course {facilitator_registration.course.name} already has an approved facilitator'
                        }, status=400)
                    
                    # Get the course and its current facilitator
                    course = facilitator_registration.course
                    current_facilitator = course.facilitators
                    
                    # Check if the course has a facilitator and if they are verified
                    if current_facilitator and current_facilitator.is_verified_facilitator:
                        # Block update if the current facilitator is verified
                        return JsonResponse({
                            'error': f'Course {course.name} already has a verified facilitator assigned'
                        }, status=400)
                    
                    # Update the course's facilitator to the new user if no verified facilitator exists
                    course.facilitators = facilitator_registration.user
                    course.save()

                    # Mark the facilitator registration as approved
                    facilitator_registration.approved = True
                    facilitator_registration.rejection_reason = None
                    facilitator_registration.rejection_timestamp = None
                    # Update the user's facilitator status
                    facilitator_registration.user.is_facilitator = True
                    facilitator_registration.user.is_verified_facilitator = True
                    facilitator_registration.user.save()
                    facilitator_registration.save()  # Save the facilitator registration
                    
                    # Send approval email to the facilitator
                    send_mail(
                        subject="Facilitator Application Approved",
                        message=f"Congratulations! Your application to facilitate {facilitator_registration.course.name} has been approved.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[facilitator_registration.user.email],
                        fail_silently=True,
                    )
                    return JsonResponse({
                        'success': f'Application for {facilitator_registration.course.name} approved',
                        'registration_id': facilitator_registration.id
                    })
                else:  # action == 'reject'
                    # Send rejection email to the facilitator
                    send_mail(
                        subject="Facilitator Application Rejected",
                        message=f"Your application to facilitate {facilitator_registration.course.name} has been rejected.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[facilitator_registration.user.email],
                        fail_silently=True,
                    )
                    facilitator_registration.delete()
                    return JsonResponse({
                        'success': f'Application for {facilitator_registration.course.name} rejected and deleted'
                    })
                    
        except Exception as e:
            logger.error(f"Error processing facilitator application: {e}")
            return JsonResponse({'error': 'Action failed'}, status=500)
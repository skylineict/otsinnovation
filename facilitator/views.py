from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Count
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course, CourseRegistration, PaymentDetail, Transaction
from .models import FacilitatorRegistration
# from .forms import FacilitatorProfileForm
from django.contrib.auth import get_user_model
import json
import uuid
from decimal import Decimal
import requests
from datetime import timedelta

User = get_user_model()

# -------------------------
# Request Facilitator View
# -------------------------
class RequestFacilitatorView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'facilitator/request_form.html', {'courses': courses})

    def post(self, request):
        course_id = request.POST.get('course')
        if not course_id:
            return JsonResponse({'error': 'Course ID is required'}, status=400)

        course = get_object_or_404(Course, id=course_id)

        if course.facilitators:
            return JsonResponse({'error': 'This course already has a facilitator'}, status=400)

        if FacilitatorRegistration.objects.filter(user=request.user, course=course).exists():
            return JsonResponse({'error': 'You have already requested for this course'}, status=400)

        FacilitatorRegistration.objects.create(
            user=request.user,
            course=course,
            approved=False
        )

        return JsonResponse({
            'status': 'success',
            'message': f'Request submitted successfully for {course.name}'
        })

# -------------------------
# Facilitator Dashboard View
# -------------------------
class FacilitatorDashboardView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        user = request.user
        is_facilitator = Course.objects.filter(facilitators=user).exists()
        facilitator_requests = FacilitatorRegistration.objects.filter(user=user)
        facilitator_course = None
        students = []

        if is_facilitator:
            facilitator_course = Course.objects.get(facilitators=user)
            students = CourseRegistration.objects.filter(course=facilitator_course, is_approved=True)

        context = {
            'is_facilitator': is_facilitator,
            'facilitator_requests': facilitator_requests,
            'facilitator_course': facilitator_course,
            'students': students,
        }

        return render(request, 'facilitator/dash.html', context)

# -------------------------
# Admin - Manage Facilitator Requests
# -------------------------
class ManageFacilitatorRequestsView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "Permission denied.")
            return redirect('login')

        pending_requests = FacilitatorRegistration.objects.filter(approved=False)
        return render(request, 'admin/manage_facilitators.html', {'pending_requests': pending_requests})

# -------------------------
# Admin - Approve/Reject Facilitator Request
# -------------------------
class ManageFacilitatorRequestView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, request_id):
        if not request.user.is_superuser:
            messages.error(request, "Permission denied.")
            return redirect('login')

        facilitator_request = get_object_or_404(FacilitatorRegistration, id=request_id)
        return render(request, 'admin/reject_facilitator.html', {'request': facilitator_request})

    def post(self, request, request_id):
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        facilitator_request = get_object_or_404(FacilitatorRegistration, id=request_id)
        course = facilitator_request.course
        action = request.POST.get('action')
        rejection_reason = request.POST.get('rejection_reason', 'Declined by admin.')

        if action not in ['approve', 'reject']:
            return JsonResponse({'error': 'Invalid action specified'}, status=400)

        if action == 'approve':
            if course.facilitators:
                return JsonResponse({'error': 'Course already has a facilitator'}, status=400)

            facilitator_request.approved = True
            facilitator_request.rejection_reason = None
            facilitator_request.save()  # Triggers FacilitatorRegistration.save() to assign facilitator

            return JsonResponse({
                'status': 'success',
                'message': 'Facilitator request approved successfully'
            })

        elif action == 'reject':
            facilitator_request.approved = False
            facilitator_request.rejection_reason = rejection_reason
            facilitator_request.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Facilitator request rejected successfully'
            })

# -------------------------
# Facilitator Students View
# -------------------------
class FacilitatorStudentsView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        try:
            course = Course.objects.get(facilitators=request.user)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'You are not assigned to any course'}, status=403)

        students = CourseRegistration.objects.filter(course=course, is_approved=True)

        return render(request, 'facilitator/students.html', {
            'course': course,
            'students': students,
        })

# -------------------------
# Student - View Course Facilitator
# -------------------------
class ViewCourseFacilitatorView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        is_registered = CourseRegistration.objects.filter(
            course=course,
            user=request.user,
            is_approved=True
        ).exists()

        if not is_registered:
            return JsonResponse({'error': 'Not registered for this course'}, status=403)

        return render(request, 'student/course_facilitator.html', {'course': course})

# -------------------------
# Facilitator Statistics
# -------------------------
class FacilitatorStatsView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        try:
            course = Course.objects.get(facilitators=request.user)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Not a facilitator'}, status=403)

        total_students = CourseRegistration.objects.filter(course=course, is_approved=True).count()
        pending_students = CourseRegistration.objects.filter(course=course, is_approved=False).count()
        training_modes = CourseRegistration.objects.filter(course=course, is_approved=True).values('training_mode').annotate(count=Count('id'))
        internship_students = CourseRegistration.objects.filter(course=course, is_approved=True, internship=True).count()

        return JsonResponse({
            'status': 'success',
            'stats': {
                'total_students': total_students,
                'pending_students': pending_students,
                'training_modes': list(training_modes),
                'internship_students': internship_students,
            }
        })

# -------------------------
# Facilitator Profile Update View
# -------------------------
class UpdateFacilitatorProfileView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        is_facilitator = Course.objects.filter(facilitators=request.user).exists()

        if not is_facilitator:
            return JsonResponse({'error': 'You are not a facilitator'}, status=403)

        # Assuming FacilitatorProfileForm is defined
        form = FacilitatorProfileForm(instance=request.user)
        return render(request, 'facilitator/update_profile.html', {'form': form})

    def post(self, request):
        is_facilitator = Course.objects.filter(facilitators=request.user).exists()

        if not is_facilitator:
            return JsonResponse({'error': 'You are not a facilitator'}, status=403)

        form = FacilitatorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully'
            })
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)

# -------------------------
# Get Facilitator Info View
# -------------------------
class GetFacilitatorInfoView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, course_id):
        try:
            course = get_object_or_404(Course, id=course_id)
            facilitators = course.facilitators.all()

            if not facilitators:
                return JsonResponse({'error': 'No facilitator assigned for this course'}, status=404)

            facilitator_info = [
                {
                    'id': facilitator.id,
                    'full_name': f"{facilitator.first_name} {facilitator.last_name}",
                    'email': facilitator.email,
                    'bio': facilitator.bio,
                    'profile_image': facilitator.profile_image.url if facilitator.profile_image else None,
                } for facilitator in facilitators
            ]

            return JsonResponse({
                'status': 'success',
                'facilitators': facilitator_info
            })

        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
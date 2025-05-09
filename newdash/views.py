from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Count
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, CourseRegistration,  PaymentDetail, Transaction
from .forms import FacilitatorProfileForm

from django.contrib.auth import get_user_model

import json
import uuid
from decimal import Decimal
import requests
from datetime import timedelta

User = get_user_model()

# Flutterwave Settings
FLW_SECRET_KEY = getattr(settings, 'FLUTTERWAVE_SECRET_KEY', None)
FLW_SECRET_HASH = getattr(settings, 'FLUTTERWAVE_HASH', None)

# -------------------------
# Utility - (Optional) Flutterwave Payment Initiator
# -------------------------
def initiate_flutterwave_payment(user, amount, tx_ref, redirect_url):
    payload = {
        "tx_ref": tx_ref,
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": redirect_url,
        "customer": {
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
        },
        "customizations": {
            "title": "Course Registration",
            "description": "Training Payment",
            "logo": "https://yourdomain.com/static/logo.png"
        }
    }

    headers = {
        "Authorization": f"Bearer {FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        'https://api.flutterwave.com/v3/payments',
        json=payload,
        headers=headers
    )

    return response.json()

# -------------------------
# Course Registration View
# -------------------------

# -------------------------
# Facilitator Request View
# -------------------------

@login_required
def request_facilitator(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)

        if course.facilitators:
            messages.error(request, "This course already has a facilitator.")
            return redirect('request_facilitator')

        if FacilitatorRegistration.objects.filter(user=request.user, course=course).exists():
            messages.warning(request, "You have already requested for this course.")
            return redirect('request_facilitator')

        FacilitatorRegistration.objects.create(
            user=request.user,
            course=course,
            approved=False
        )

        messages.success(request, f"Request submitted successfully for {course.name}.")
        return redirect('facilitator_dashboard')

    return render(request, 'facilitator/request_form.html', {'courses': courses})

# -------------------------
# Facilitator Dashboard View
# -------------------------
@login_required
def facilitator_dashboard(request):
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

    return render(request, 'facilitator/dashboard.html', context)

# -------------------------
# Admin - Manage Facilitator Requests
# -------------------------
@login_required
def manage_facilitator_requests(request):
    if not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('home')

    pending_requests = FacilitatorRegistration.objects.filter(approved=False)
    return render(request, 'admin/manage_facilitators.html', {'pending_requests': pending_requests})

@login_required
def approve_facilitator_request(request, request_id):
    if not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('home')

    facilitator_request = get_object_or_404(FacilitatorRegistration, id=request_id)
    course = facilitator_request.course

    if course.facilitators:
        messages.error(request, "Course already has a facilitator.")
        return redirect('manage_facilitator_requests')

    facilitator_request.approved = True
    facilitator_request.save()

    messages.success(request, "Facilitator request approved.")
    return redirect('manage_facilitator_requests')

@login_required
def reject_facilitator_request(request, request_id):
    if not request.user.is_superuser:
        messages.error(request, "Permission denied.")
        return redirect('home')

    facilitator_request = get_object_or_404(FacilitatorRegistration, id=request_id)

    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'Declined by admin.')
        facilitator_request.approved = False
        facilitator_request.rejection_reason = reason
        facilitator_request.save()
        messages.success(request, "Facilitator request rejected.")
        return redirect('manage_facilitator_requests')

    return render(request, 'admin/reject_facilitator.html', {'request': facilitator_request})

# -------------------------
# Facilitator Students View
# -------------------------
@login_required
def facilitator_students(request):
    try:
        course = Course.objects.get(facilitators=request.user)
    except Course.DoesNotExist:
        messages.error(request, "You are not assigned to any course.")
        return redirect('facilitator_dashboard')

    students = CourseRegistration.objects.filter(course=course, is_approved=True)

    return render(request, 'facilitator/students.html', {
        'course': course,
        'students': students,
    })

# -------------------------
# Student - View Course Facilitator
# -------------------------
@login_required
def view_course_facilitator(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    is_registered = CourseRegistration.objects.filter(
        course=course,
        user=request.user,
        is_approved=True
    ).exists()

    if not is_registered:
        messages.error(request, "Not registered for this course.")
        return redirect('student_dashboard')

    return render(request, 'student/course_facilitator.html', {'course': course})

# -------------------------
# Facilitator Statistics
# -------------------------
@login_required
def facilitator_stats(request):
    try:
        course = Course.objects.get(facilitators=request.user)
    except Course.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not a facilitator'}, status=403)

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
@login_required
def update_facilitator_profile(request):
    is_facilitator = Course.objects.filter(facilitators=request.user).exists()

    if not is_facilitator:
        messages.error(request, "You are not a facilitator.")
        return redirect('facilitator_dashboard')

    if request.method == 'POST':
        form = FacilitatorProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('facilitator_dashboard')
    else:
        form = FacilitatorProfileForm(instance=request.user)

    return render(request, 'facilitator/update_profile.html', {'form': form})

# -------------------------
# Get Facilitator Info View
# -------------------------
@login_required
def get_facilitator_info(request, course_id):
    try:
        course = get_object_or_404(Course, id=course_id)

        facilitators = course.facilitators.all()

        if not facilitators:
            return JsonResponse({'status': 'error', 'message': 'No facilitator assigned for this course.'}, status=404)

        facilitator_info = []
        for facilitator in facilitators:
            facilitator_info.append({
                'id': facilitator.id,
                'full_name': f"{facilitator.first_name} {facilitator.last_name}",
                'email': facilitator.email,
                'bio': facilitator.bio,
                'profile_image': facilitator.profile_image.url if facilitator.profile_image else None,
            })

        return JsonResponse({
            'status': 'success',
            'facilitators': facilitator_info
        })

    except Course.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Course not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
def payment_success(request):
    return render(request, 'payment_success.html') 
 # -------------------------
# Flutterwave Webhook Handler
# -------------------------
def flutterwave_webhook(request):
    try:
        # Flutterwave sends the data in JSON format, so we parse it
        payload = json.loads(request.body)

        # You can add logic to process the webhook payload
        # Check if the payment was successful
        if payload['status'] == 'successful':
            # Handle the successful payment (e.g., update the database, send confirmation)
            transaction_id = payload['tx_ref']
            # Process the payment (example: update user's registration status)
            # For instance:
            # registration = CourseRegistration.objects.get(transaction_id=transaction_id)
            # registration.payment_status = 'success'
            # registration.save()

            return JsonResponse({'status': 'success', 'message': 'Payment was successful'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Payment failed'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
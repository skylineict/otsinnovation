from django.shortcuts import render, redirect
from django.http import JsonResponse
from  courses.models import CourseRegistration, Course, PaymentDetail, Transaction
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import pdb
from django.contrib.auth.decorators import login_required
@login_required
def fetch_all_courses(request):
    courses = Course.objects.all().order_by('name')  # Optional: order alphabetically by name

    course_list = list(courses.values('id', 'name', 'description', 'amount'))

    return JsonResponse({
        "courses": course_list
        
    })





class CourseRegistrationView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self, request):
        courses = Course.objects.all()
        existing_registration = CourseRegistration.objects.filter(user=request.user).first()
        return render(request, 'dashboard/coursespage/courses_registration.html', {'courses': courses,
        'registration': existing_registration})

    def post(self, request):
        # Get form data
        full_name = request.POST.get('fullname')
        course_id = request.POST.get('course')
        training_mode = request.POST.get('trainingMode')
        internship = request.POST.get('internship') == 'on'
        

        # Check for empty fields
        if not full_name or not course_id or not training_mode:
            return JsonResponse({'error': "All fields are required."}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'error': "Invalid course selected."}, status=400)
        
        existing = CourseRegistration.objects.filter(user=request.user)
        if existing.exists():
            return JsonResponse({'error': 'You have already registered for a course'}, status=400)

      

        # Create CourseRegistration
        course_registration = CourseRegistration.objects.create(
            full_name=full_name,
            course=course,
            training_mode=training_mode,
            internship=internship,
            user=request.user
        )

      
           # Prepare success response
        return JsonResponse({
            'success': 'Course Registration Successful',
            'course': {
                'name': course.name,
                'duration': course.duration,
                'amount': course.amount,
                'facilitator': course.facilitators.get_full_name(),
            },
            'training_mode': course_registration.training_mode,
            'internship': course_registration.internship,
            'is_approved': course_registration.is_approved
        })
    
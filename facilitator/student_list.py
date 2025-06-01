from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from courses.models import Course, CourseRegistration
from registration.models import MyUser

class FacilitatorStudentsView(LoginRequiredMixin, View):
    login_url = 'login'

    def test_func(self):
        # Check if the user is a verified facilitator
        return self.request.user.is_facilitator and self.request.user.is_verified_facilitator

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        if not self.test_func():
            return redirect('login')
       
        facilitated_courses = request.user.facilitated_course

       
        student_registrations =CourseRegistration.objects.filter(
    course=facilitated_courses,
    account_suspended=False
        ).select_related('course', 'user', 'user__profiles', 'payment_detail').prefetch_related('payment_detail__transactions')

       
        registrations_with_cohort = []
        for registration in student_registrations:
            cohort = registration.user.cohorts.filter(course=registration.course).first()
            registration.cohort_name = cohort.name if cohort else None
            registrations_with_cohort.append(registration)
       
        return render(request, 'facilitator/student_list.html', {
            'students': student_registrations
        })
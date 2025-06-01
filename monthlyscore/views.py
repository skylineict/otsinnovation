from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import CourseMonthlyRequirement
from courses.models import Course
from django.utils import timezone

class CourseListAPIView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # Restrict access to staff or facilitator users
        if not (request.user.is_staff or request.user.is_facilitator):
            return JsonResponse({
                'success': False,
                'error': 'Unauthorized access.'
            }, status=403)

        # Get courses the user can manage
        if request.user.is_staff:
            courses = Course.objects.all()
        else:
            courses = Course.objects.filter(facilitators=request.user)

        # Serialize courses to JSON
        course_list = [{'id': course.id, 'name': course.name} for course in courses]

        return JsonResponse({
            'success': True,
            'courses': course_list
        })

# View for facilitators to create or view monthly score requirements
class MonthlyRequirementView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request):
        if not (request.user.is_staff or request.user.is_facilitator):
            logout(request)
            return redirect('login')

        try:
            course_id = request.POST.get('course_id')
            score_requirement = request.POST.get('score_requirement')

            if not all([course_id, score_requirement]):
                return JsonResponse({
                    'success': False,
                    'error': 'Missing required fields: course_id and score_requirement are required.'
                }, status=400)
            try:
                course = Course.objects.get(id=course_id)
                if not (request.user.is_staff or course.facilitators == request.user):
                    return JsonResponse({
                        'success': False,
                        'error': 'You are not authorized to set a score for this course.'
                    }, status=403)
            except Course.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Course not found.'
                }, status=400)

            try:
                score_requirement = int(score_requirement)
                if score_requirement <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Score requirement must be a positive integer.'
                }, status=400)

            current_date = timezone.now().date()
            print(f"Current date: {current_date}")
            month_date = month_date = current_date.replace(day=1)
            print(f"Month date: {month_date}")
            existing_requirement = CourseMonthlyRequirement.objects.filter(course=course).order_by('-month').first()

            if existing_requirement:
                existing_requirement.reset_if_expired(current_date)
                if existing_requirement.month == month_date and existing_requirement.score_requirement > 0:
                    return JsonResponse({
                        'success': False,
                        'error': f'A monthly score requirement already exists for {course.name} - {month_date.strftime("%B %Y")}.'
                    }, status=400)

            # Create new requirement
            monthly_requirement = CourseMonthlyRequirement.objects.create(
                course=course,
                month=month_date,
                score_requirement=score_requirement,
                is_approved=False
            )

            return JsonResponse({
                'success': True,
                'message': f'Monthly score requirement created for {course.name} - {month_date.strftime("%B %Y")}. Awaiting staff approval.'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

# # View for staff to approve monthly score requirements
# class ApproveMonthlyRequirementView(LoginRequiredMixin, View):
#     login_url = 'login'


    
#     def get(self, request):
#         if not request.user.is_staff:
#             logout(request)
#             return redirect('login')
#         monthly_requirements = CourseMonthlyRequirement.objects.filter(is_approved=False)

      

#         context = {
#             'monthly_requirements': monthly_requirements
#         }
#         return render(request, 'admindash/monthlyscore/monthlysocre.html', context)

#     def post(self, request):
#         # Restrict access to staff users only
#         if not request.user.is_staff:
#             logout(request)
#             return redirect('login')

#         try:
#             # Check for single action (single ID)
#             requirement_id = request.POST.get('requirement_id')

#             if requirement_id:
#                 # Single approval
#                 try:
#                     requirement = CourseMonthlyRequirement.objects.get(id=requirement_id, is_approved=False)
#                     requirement.approve(request.user)
#                     return JsonResponse({
#                         'success': True,
#                         'message': f'Monthly requirement for {requirement.course.name} - {requirement.month.strftime("%B %Y")} approved successfully.'
#                     })
#                 except CourseMonthlyRequirement.DoesNotExist:
#                     return JsonResponse({
#                         'success': False,
#                         'error': 'Requirement not found or already approved.'
#                     }, status=400)

#             else:
#                 return JsonResponse({
#                     'success': False,
#                     'error': 'No requirement specified.'
#                 }, status=400)

#         except Exception as e:
#             return JsonResponse({
#                 'success': False,
#                 'error': str(e)
#             }, status=500)
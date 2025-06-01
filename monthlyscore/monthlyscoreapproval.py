from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from .models import CourseMonthlyRequirement
from django.utils import timezone

class ApproveMonthlyRequirementView(LoginRequiredMixin, View):

    login_url = 'login'

    def get(self, request):
        if not request.user.is_staff:
            logout(request)
            return redirect('login')
        monthly_requirements = CourseMonthlyRequirement.objects.filter(is_approved=False)
        context = {
            'monthly_requirements': monthly_requirements
        }
        return render(request, 'admindash/monthlyscore/monthlyscore.html', context)

    def post(self, request):
        if not request.user.is_staff:
            logout(request)
            return redirect('login')

        try:
            requirement_id = request.POST.get('requirement_id')
            action = request.POST.get('action')

            if not requirement_id or not action:
                return JsonResponse({
                    'success': False,
                    'error': 'Requirement ID and action are required.'
                }, status=400)

            try:
                requirement = CourseMonthlyRequirement.objects.get(id=requirement_id)
            except CourseMonthlyRequirement.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Requirement not found.'
                }, status=400)

            if action == 'approve':
                if requirement.is_approved:
                    return JsonResponse({
                        'success': False,
                        'error': 'Requirement is already approved.'
                    }, status=400)
                requirement.approve(request.user)
                return JsonResponse({
                    'success': True,
                    'message': f'Monthly requirement for {requirement.course.name} - {requirement.month.strftime("%B %Y")} approved successfully.'
                })
            elif action == 'reject':
                course_name = requirement.course.name
                month_str = requirement.month.strftime("%B %Y")
                requirement.delete()
                return JsonResponse({
                    'success': True,
                    'message': f'Monthly requirement for {course_name} - {month_str} rejected and removed.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid action specified.'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from courses.models import CourseRegistration,Course
from registration.models import MyUser
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class FilterByCourseView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        course_id = request.GET.get('course_id', '').strip()
        page = request.GET.get('page', '1').strip()

        if not course_id:
            return JsonResponse({'error': 'Course ID is required'}, status=400)

        try:
            registrations = CourseRegistration.objects.filter(
                is_approved=False,
                course_id=course_id
            ).select_related('course', 'user')
            logger.info(f"Filter by course_id='{course_id}' by {request.user.email} returned {len(registrations)} registrations.")

            # Paginate
            paginator = Paginator(registrations, 10)  # 10 items per page
            try:
                page_obj = paginator.page(page)
            except ValidationError:
                page_obj = paginator.page(1)

            data = [{
                'id': reg.id,
                'full_name': reg.full_name,
                'username': reg.user.username if reg.user else 'N/A',
                'course_name': reg.course.name,
                'training_mode': reg.training_mode,
                'is_approved': reg.is_approved,
            } for reg in page_obj]

            return JsonResponse({
                'success': True,
                'student_list': data,
                'pagination': {
                    'total_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_previous': page_obj.has_previous(),
                    'has_next': page_obj.has_next(),
                },
                'message': f'Found {len(data)} registrations (page {page_obj.number})'
            })
        except Exception as e:
            logger.error(f"Filter error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        


def list_courses(request):
    if request.method == 'GET':
        try:
            courses = Course.objects.all().values('id', 'name')
            return JsonResponse({'list_courses': list(courses)}, status=200)
        except Exception:
            return JsonResponse({'error': 'Failed to fetch courses'}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
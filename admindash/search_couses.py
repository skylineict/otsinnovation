from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from courses.models import CourseRegistration
from registration.models import MyUser
from django.core.paginator import Paginator
from django.db.models import Q
import logging


class UserSearchApprovalView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        query = request.GET.get('query', '').strip()
        page = request.GET.get('page', '1').strip()

        if not query:
            return JsonResponse(
                {'success': False, 'error': 'Search term is required'},
                status=400
            )

        try:
            # Use OR condition for username or course_name
            search_query = (
                Q(user__username__icontains=query) |
                Q(course__name__icontains=query)
            )
            query = Q(is_approved=False) & search_query

            registrations = CourseRegistration.objects.filter(query).select_related('course', 'user')
           

            # Paginate
            paginator = Paginator(registrations, 10)
            try:
                page_obj = paginator.page(page)
            except:
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
            }, status=200)
        except Exception as e:
           
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
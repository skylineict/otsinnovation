from venv import logger
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from courses.models import CourseRegistration
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import logging

# return render(request, 'admindash/courses/approval.html', context)

class CourseRegistrationApprovalView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/login/'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('login')

    def get(self, request):
        logger.debug(f"Request headers: {request.headers}")
        page = request.GET.get('page', '1').strip()
        registrations = CourseRegistration.objects.filter(is_approved=False).select_related('course', 'user')
        paginator = Paginator(registrations, 1)  
        try:
            page_obj = paginator.page(page)
        except ValidationError:
            page_obj = paginator.page(1)



        # Check if the request is AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Prepare JSON response for AJAX
            student_list = [
                {
                    'id': reg.id,
                    'full_name': reg.user.get_full_name() or 'N/A',
                    'username': reg.user.username,
                    'course_name': reg.course.name,
                    'training_mode': reg.training_mode,
                    'is_approved': reg.is_approved
                } for reg in page_obj
            ]

       
            pagination = {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next()
            }
            return JsonResponse({
                'success': True,
                'student_list': student_list,
                'pagination': pagination,
                'message': 'Registrations fetched successfully'
            })

       
        context = {
            'pending_registrations': page_obj,
        }
        return render(request, 'admindash/courses/approval.html', context)
       

    def post(self, request):
        try:
            action = request.POST.get('action')
            registration_ids = request.POST.getlist('registration_ids[]')
            registration_id = request.POST.get('registration_id')

            if action not in ['approve', 'reject']:
                return JsonResponse({'success': False, 'error': 'Invalid action specified.'}, status=400)

            if registration_ids:
                if action == 'approve':
                    updated_count = 0
                    for reg_id in registration_ids:
                        try:
                            registration = CourseRegistration.objects.get(id=reg_id, is_approved=False)
                            registration.manual_approve(admin_user=request.user)
                            updated_count += 1
                        except (CourseRegistration.DoesNotExist, ValidationError) as e:
                            
                            continue
                    if updated_count:
                        return JsonResponse({'success': True, 'message': f'{updated_count} registration(s) approved successfully.'})
                    return JsonResponse({'success': False, 'error': 'No valid pending registrations selected.'}, status=400)
                else:
                    deleted_count = CourseRegistration.objects.filter(id__in=registration_ids, is_approved=False).delete()[0]
                    if deleted_count:
                      
                        return JsonResponse({'success': True, 'message': f'{deleted_count} registration(s) rejected and deleted successfully.'})
                    return JsonResponse({'success': False, 'error': 'No valid pending registrations selected.'}, status=400)

            elif registration_id:
                if action == 'approve':
                    try:
                        registration = CourseRegistration.objects.get(id=registration_id, is_approved=False)
                        registration.manual_approve(admin_user=request.user)
                        return JsonResponse({'success': True, 'message': 'Registration approved successfully.'})
                    except CourseRegistration.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Registration not found or already approved.'}, status=400)
                    except ValidationError as e:
                       
                        return JsonResponse({'success': False, 'error': str(e)}, status=400)
                else:
                    try:
                        registration = CourseRegistration.objects.get(id=registration_id, is_approved=False)
                        registration.delete()
                      
                        return JsonResponse({'success': True, 'message': 'Registration rejected and deleted successfully.'})
                    except CourseRegistration.DoesNotExist:
                        return JsonResponse({'success': False, 'error': 'Registration not found or already processed.'}, status=400)

            else:
                return JsonResponse({'success': False, 'error': 'No registrations specified.'}, status=400)

        except Exception as e:
           
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
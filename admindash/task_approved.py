from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Task_collections

class TaskApprovalView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        # Restrict access to staff or facilitator users
        if not (request.user.is_staff or request.user.is_facilitator):
            return redirect('login')

        # Fetch all pending task submissions
        pending_tasks = Task_collections.objects.filter(status='pending').select_related('student')

        context = {
            'pending_tasks': pending_tasks,
        }
        return render(request, 'admindash/student_task/task_approval.html', context)

    def post(self, request):
        # Restrict access to staff or facilitator users
        if not (request.user.is_staff or request.user.is_facilitator):
            return JsonResponse({'error': 'Unauthorized access.'}, status=403)

        try:
            # Check for bulk approval (list of IDs)
            task_collection_ids = request.POST.getlist('task_collection_ids[]')
            # Check for single approval (single ID)
            task_collection_id = request.POST.get('task_collection_id')

            if task_collection_ids:
                # Bulk approval
                updated_count = Task_collections.objects.filter(
                    id__in=task_collection_ids,
                    status='pending'
                ).update(status='complete')

                if updated_count > 0:
                    return JsonResponse({
                        'success': True,
                        'message': f'{updated_count} task(s) approved successfully.'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'No valid pending tasks selected.'
                    }, status=400)

            elif task_collection_id:
                # Single approval
                try:
                    task_collection = Task_collections.objects.get(
                        id=task_collection_id,
                        status='pending'
                    )
                    task_collection.status = 'complete'
                    task_collection.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Task approved successfully.'
                    })
                except Task_collections.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Task not found or already approved.'
                    }, status=400)

            else:
                return JsonResponse({
                    'success': False,
                    'error': 'No task IDs provided.'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
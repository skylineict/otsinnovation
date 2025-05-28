from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Task_collections, Task

User = get_user_model()

class CreateTaskView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self,request):
        if not request.user.is_staff:
            return redirect('login')
        return render(request, 'admindash/student_task/task.html')



    def post(self, request):
        if not request.user.is_staff:
            return redirect('login')

        task = request.POST.get('task')
        links = request.POST.get('links')
        task_description = request.POST.get('task_description')
        task_img = request.FILES.get('task_img')

        print(task, links, task_description, task_img)

        if not task or not links or not task_img:
            return JsonResponse({'error': 'Missing required fields'
            }, status=400)
        

        existing_task = Task.objects.filter(task=task, links=links).exists()
        
        if existing_task:
            return JsonResponse({'error': 'Task with this title and link already exists'
            }, status=400)
        Task.objects.create(
        task=task,
        links=links,
        task_description=task_description,
        task_img=task_img
    )

        return JsonResponse({
            'status': 'success',
            'message': f'Task assigned to  students successfully'
        })

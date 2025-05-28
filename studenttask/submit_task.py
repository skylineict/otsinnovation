from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task_collections, Task
import pdb
from django.http import JsonResponse



#New Task Collection by Da'Guy
class Taskscollection(LoginRequiredMixin,View):
    login_url = 'login'
    
    def get(self,request):
        total_task = Task.objects.all().count()
        task_collection =  Task_collections.objects.filter(student=request.user)[:4]
        task =  Task.objects.all()
        all_pending_task =  task =  Task.objects.all()
        approved_task_count = Task_collections.objects.filter(status='complete', student=request.user).count()
        
        
        context = {
            'total_task': total_task,
            'task': task,
            'task_collection':task_collection,
            'approved_task_count':approved_task_count,
            'allcohorts':all_pending_task,
        }
        
        return render(request, 'dashboard/task/task_collection.html', context=context)
    
    from django.http import JsonResponse

    def post(self, request):
            task_collection = request.POST.get('project')
            link = request.POST.get('url')
            screen_short = request.FILES.get('myfiles')



            if not task_collection or not link or not screen_short:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
         
        

            # Check if the task has already been submitted by this user
            submitted_task = Task_collections.objects.filter(
                task=task_collection, 
                student=request.user
            ).exists()

            if submitted_task:
                return JsonResponse({'error': 'You have already submitted this task.'}, status=400)

            # Create the task if not already submitted
            Task_collections.objects.create(
                task=task_collection,
                links=link,
                screen_short=screen_short,
                student=request.user,
                status='pending'
            )

            return JsonResponse({'success': 'Task submitted successfully!'}, status=200)



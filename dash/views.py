from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profiles
from django.core.exceptions import ObjectDoesNotExist
from cohorts.models import Cohort
from .models  import Mypasscode
from django.contrib import messages
from .models import Payment
from studenttask.models import Task_collections, Task
from django.core.mail import send_mail
import pdb
from portal.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator


# studentcode = None
# cohorts = None
# Create your views here.



class Dashboard(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user

        # Fetch Profile only once
        try:
            myprofile = Profiles.objects.get(user=user)
        except Profiles.DoesNotExist:
            return redirect('profile')

        # Check if Assignment exists and handle redirection
        # assign = Assigment.objects.filter(user=user).first()
        # if assign and assign.score_project < 15:
        #     return redirect('reating')

       

        # Fetching student's task collection (max 4)
        task_collection = Task_collections.objects.filter(student=user)[:4]
        # if task_collection.count() != 10:
        #     return redirect('task_collwction')

        

   
        # Context Data
        context = {
            
            'profile': myprofile,

            'task': task_collection,
        }
           

      
        return render(request, 'dashboard/dash.html', context)

    def post(self, request):
        return render(request, 'dashboard/dash.html')








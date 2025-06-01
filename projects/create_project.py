from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profiles
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from studenttask.models import Task_collections,Task
from django.core.mail import send_mail
import pdb
from portal.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProjectVeiw(LoginRequiredMixin, View):
    login_url = 'login' 
    
    

    def get(self, request):
        if not (request.user.is_staff or request.user.is_facilitator):
            return redirect('login') 
        return render(request, 'admindash/projects/create_projects.html')

    def post(self, request):
        return render(request, 'admindash/projects/create_projects.html')

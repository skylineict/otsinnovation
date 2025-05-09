from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from projects.forms import TaskForm
from .models import Project, Assigment, Task
from dash.models import Payment,Cohorts
from django.contrib import messages
from django.contrib.auth.models import User
from userprofile.models import Profiles
from .form import bodyform
from .models import Task_collections
from django.urls import reverse_lazy, reverse
import pdb


# Create your views here.


class Projects(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        # try:
        #      payments= Payment.objects.get(user=request.user)
        # except: payments =  None
        projects = Project.objects.filter(status='active')
        expired_projects = Project.objects.filter(status='expired')
        try:
            myprofile = Profiles.objects.get(user=request.user)
        except: myprofile = None


        try:
            assign = Assigment.objects.get(user=request.user)
            if assign.score_project < 15:
                return  redirect('reating')
        except: assign = None
        # fullstack = Recapsesion.objects.filter(courses__name='Full-Stack Engineering')
        # front_end = Recapsesion.objects.filter(courses__name='Front-end Engineering')
        return render(request, 'dashboard/project.html',{'myprofile':myprofile,'projects':projects, 'expired_projects': expired_projects})

        
    def post(self,request):
        return render(request, 'dashboard/project',{})
    


class Create_Projects(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
      form = bodyform
      return render(request, 'dashboard/project_form.html',{'form':form})

        
    def post(self,request):
        descrip = bodyform(request.POST)
        project_name =  request.POST['project']
        start_date =     request.POST['start_date']
        end_date   =     request.POST['end_date']
        
        create_myproject = Project.objects.create(project_name=project_name,start_date=start_date,ending_date=end_date)
        create_myproject.descriptions =descrip
        create_myproject.save()
        messages.success(request,"project created successfully")
        return render(request, 'dashboard/project_form.html',{})



class Projects_datials(View):
    def get(self,request, pk):
        projects_datials = Project.objects.get(pk=pk)
        expired_projects = Project.objects.filter(status='expired')
        active_projects = Project.objects.filter(status='active')
        
        context = {
            'projects_datial' :projects_datials, 
            'expired_projects': expired_projects,
            ' active_projects': active_projects
        }
        return render(request, 'dashboard/project_details.html', context=context)
    
    
    
    def post(self, request, pk):
        projects_datials = Project.objects.get(pk=pk)
        expired_projects = Project.objects.filter(status='expired')
        return render(request, 'dashboard/project_details.html', {' projects_datial': projects_datials})
    
   
#    payment = (
#     ('pending', "pending"),
#     ('approved', "approved"),
#     ('reject', "reject"),
# )
    
#here is pending payment views 
class Payment_approval(View):
    def get(self, request):
        payment_materials = Payment.objects.filter(payment_status="approved")
        pending_approval = Payment.objects.filter(payment_status="pending")
        return render(request, "dashboard/pending_payment.html", {'payment_materials':payment_materials,'pending_approval':pending_approval})
        
        
    def post(self, request):
        return render(request, "dashboard/pending_payment.html")



class Payment_jected(View):
    def get(self, request):
        payment_materials = Payment.objects.filter(payment_status="reject")
        pending_approval = Payment.objects.filter(payment_status="pending")
        return render(request, "dashboard/payment_reject.html", {'payment_materials':payment_materials,'pending_approval':pending_approval})
        
        
    def post(self, request):
        return render(request, "dashboard/payment_reject.html")
    
    

#here is approved payment views 

class Pending_payment(View):
    def get(self, request):
        payment_materials = Payment.objects.filter(payment_status="approved")
        pending_approval = Payment.objects.filter(payment_status="pending")
        return render(request, "dashboard/payment_approval.html", {'payment_materials':payment_materials,'pending_approval':pending_approval})
        
        
    def post(self, request):
        return render(request, "dashboard/payment_approval.html")
    
class view_payment(View):
    def get(self,request, pk):
        projects_datials = Payment.objects.get(pk=pk)
     
        return render(request, 'dashboard/view_payment.html', {'view_payment' :projects_datials,})
    
    
    
    def post(self, request, pk):
        return render(request, 'dashboard/view_payment.html', {})
   
    
class Submitassigment(View):
    def get(self,request):
        active_projects = Project.objects.filter(status='active')
        # filternow = Assigment.objects.filter(project__status='active')
        
       
        try:
             cohorts = Cohorts.objects.get(users=request.user)
             
        except:cohorts=  None
        
        try:
             
             passcode = Payment.objects.get(user=request.user).passcode
        except:passcode =  None
        
        
        return render(request, 'dashboard/assigmentsubmision.html', {'cohorts':cohorts, 'passcode':passcode, 'myassigment':active_projects, })
    
    
    
    def post(self, request):
      
        project_title = request.POST['project']
        git_hub = request.POST['url']
        passcod     = request.POST['passcode']
        
        try:
             cohorts = Cohorts.objects.get(users=request.user)
             
        except:cohorts=  None
        
        
      
       
        if Assigment.objects.filter(project=project_title,user=request.user).exists():
            messages.error(request, "multiple submissions of the same assignment are not permitted ")
            return render(request, 'dashboard/assigmentsubmision.html')
        assigment = Assigment.objects.create(passcode=passcod, project=project_title,git_hub=git_hub,cohorts=cohorts,user=request.user)
        assigment.status = 'reviewing'
       
        

        assigment.save()
        messages.success(request, "assigment submited sucessfully")
        return  redirect('dash')
        
        # return render(request, 'dashboard/assigmentsubmision.html', {})
   


def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_admin)


  
class Assigment_approval(View):
    def get(self,request):
     
        
        assigment_review = Assigment.objects.filter(status='reviewing ')
        complete_assigment = Assigment.objects.filter(status='complete')
        
        try:
            review = Assigment.objects.get(status='reviewing')
        
        except: review = None
        context = {
            'assigment_review':assigment_review,
            'complete_assigment':complete_assigment,
            'review': review
        }
        # pdb.set_trace()
        return render(request, "dashboard/assigment.html", context=context)
    
    
    def post(self,request):
        return render(request, "dashboard/assigment.html")
    

class Approve_project(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        
        projects = Project.objects.filter(status='pending')
        expired_projects = Project.objects.filter(status='expired')
    
        return render(request, 'dashboard/project_approval.html',{'projects':projects, 'expired_projects': expired_projects})

        
    def post(self,request):
        return render(request, 'dashboard/project_approval.html',{})
    
    
    
class Task_approval(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        
        # all_task = Task_collections.objects.all()
        
        task_pending = Task_collections.objects.filter(status='pending')
        
       
        
        return render(request, "dashboard/task_approval.html",{'task_collections':task_pending})
    
    
    def post(self,request):
        return render(request, "dashboard/task_approval.html")
    
def approved_task(request, pk):
    task_get = Task_collections.objects.get(pk=pk)
    task_get.status = 'complete'
    task_get.save()
    messages.success(request, 'task approved Sucessfully ')
    return redirect('task_me')




class RatingScore(View):
    def get(self,request):
        return render(request,'rating.html')
    

    
    def post(self,request):
        return render(request,'rating.html')
    
    
    

    

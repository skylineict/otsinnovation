from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profiles
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from dash.models import Payment
from projects .models import Assigment, Project
from projects .models import  Task_collections
from django.core.mail import send_mail
import pdb
from portal.settings import EMAIL_HOST_USER
from projects.models import Project
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DashAdmin(LoginRequiredMixin, View):
    login_url = 'login'  
    # def test_func(self):
    #     return self.request.user.is_staff

    # def handle_no_permission(self):
    #     return redirect('login')

    def get(self, request):
        return render(request, 'admindash/dash.html')

    def post(self, request):
        return render(request, 'admindash/dash.html')

    
    
    
    
   #this is code line for approved view  
def approved(request, pk):
    payment_approved = Payment.objects.get(pk=pk)
    

    payment_approved.payment_status = 'approved'
    payment_approved.mysave()
    payment_approved.save()
    subject = "Payment Approved"
    body = "hello payment has being approved"
    from_email = EMAIL_HOST_USER
    toemail =  [payment_approved.user.email]
    send_now =send_mail(subject, body,from_email, toemail)
    if send_now:
        messages.success(request, "email sent to user sucessfully ")
    
    messages.success(request, "payment appoved sucessful")
    return redirect('payment_approval')


#reject payment users in django 
#pyment rehections
def payment_reject(request, pk):
    payment_approved = Payment.objects.get(pk=pk)
    

    payment_approved.payment_status = 'reject'
    payment_approved.save()
    subject = "Courses Material Declined"
    body = "Hi buddy, payment for course materials has been declined. Contact the administrator with your proof of payment."
    from_email = EMAIL_HOST_USER
    toemail =  [payment_approved.user.email]
    send_now =send_mail(subject, body,from_email, toemail)
    if send_now:
        messages.success(request, "email sent to user sucessfully ")
    
    messages.success(request, "payment appoved sucessful")
    return redirect('payment_approval')




class Pending_student(View):
    def get(self, request):
        pending_approval = Profiles.objects.filter(status="pending")
        
        paginator = Paginator(pending_approval, 2) #showing just 4 page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        return render(request, "dashboard/adminssion_approval.html", {'page_obj':page_obj})
        
        
    def post(self, request):
        return render(request, "dashboard/adminssion_approval.html")


def approved_admission(request, pk):
    admissioin_approved = Profiles.objects.get(pk=pk)
    admissioin_approved.status = 'admitted'
    admissioin_approved.save()
    subject = "Congratulations, you’ve been accepted to the Obidients Tech Space for Software Engineering Programme"
    text = "Welcome "
    from_email = EMAIL_HOST_USER
    toemail =  [admissioin_approved.user.email]
    current_site = get_current_site(request)
    context = {
        
        'admissioin_approved':admissioin_approved ,
        'current_site':   current_site
    }
    
    html_message = render_to_string(
                    template_name='dashboard/email.html', context=context)
    mysend = EmailMultiAlternatives( subject, text, from_email, toemail)
    mysend.attach_alternative(html_message, 'text/html')
    mysend.send()
    
  
    messages.success(request, "email sent to user sucessfully")
    return redirect('pending')



def myapproved(request, pk):
    assign = Assigment.objects.get(pk=pk)
    assign.status = 'complete'
    assign.score_project =+10
    # assignment.student.score += 1
    assign.save()
    subject = "Assignment submission"
    body = f"Hi buddy, {assign.user},The assignment submission has been approved and the score has been credited to your dashboard."
    from_email = EMAIL_HOST_USER
    toemail =  [ assign.user.email]
    send_now =send_mail(subject, body,from_email, toemail)
    if send_now:
         messages.success(request, "email sent to user sucessfully")


def rejectassigment(request, pk):
    assign = Assigment.objects.get(pk=pk)
    assign.delete()
    # assignment.student.score += 1
    subject = "Assignment Rejected"
    body = f"Hi buddy, {assign.user},The assignment submitted was rejected, please review your assignment and submit it within 24 hours."
    from_email = EMAIL_HOST_USER
    toemail =  [ assign.user.email]
    send_now =send_mail(subject, body,from_email, toemail)
    if send_now:
        messages.success(request, "email sent to user sucessfully")
    return redirect('assigment_approval')




def approved_myproject(request, pk):
    project_approved = Project.objects.get(pk=pk)
    project_approved.status = "active"
    project_approved.save()
    admitted = Profiles.objects.filter(status='admitted')
    subject = "A new project is now available"
    from_email = EMAIL_HOST_USER
    text = "Welcome "
    current_site = get_current_site(request)
    context = {
        
        'project':project_approved ,
        'current_site':   current_site
    }
    html_message = render_to_string(
                    template_name='dashboard/email_project.html', context=context)
    
  
        
    for admit in admitted:
        toemail = admit.user.email
        mysend = EmailMultiAlternatives( subject, text, from_email, [toemail])
        mysend.attach_alternative(html_message, 'text/html')
        mysend.send()
        # send_mail(subject, body,from_email, [toemail])
    messages.success(request, "email sent to user sucessfully ")
    return redirect('pending')


from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from portal.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from userprofile.models import Profiles
from django.template.loader import render_to_string
from django.core.mail import send_mail




# Create your views here.

class Messages(View):
    def get(self, request):
        admitted = Profiles.objects.filter(status='admitted')
        

        return render(request, 'dashboard/send_email.html' , {'admitted':admitted})
        


    def post(self,request):
      
        
        subject = request.POST['subject']
        body = request.POST['message']
        from_email = EMAIL_HOST_USER
        admitted = Profiles.objects.filter(status='admitted')
        html_message = render_to_string(
                    template_name='dashboard/sendemail.html')
        
      
       
        for admitted in admitted:
            tosend = admitted.user.email
            mysend = EmailMultiAlternatives( subject, body, from_email, [tosend])
            mysend.attach_alternative(html_message, 'text/html')
        if  mysend.send():
            messages.success(request, "email sent to user sucessfully ")


        



        
        
        
        return render(request, 'dashboard/send_email.html')




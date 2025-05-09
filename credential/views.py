from django.shortcuts import render,reverse,redirect
from django.views.generic import View
from registration.models import MyUser
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from userprofile.models import Profiles
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from portal.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail



# Create your views here.


class Forgetphone(View):
    def get(self, request):
        return render(request, 'registration/phone.html')
    
    
    def post(self, request):
        email = request.POST['email']
       
        
        try: 
            
            myemails = MyUser.objects.get(email=email)
        except ObjectDoesNotExist:
            myemails = None
            messages.error(request, 'No email records found, please try again')
            
            
        if myemails:
            messages.success(request, f"Hi, your WhatsApp login number is {myemails.phone}, Login to continue")
            return render(request, 'registration/phone.html')
        # else:
        #     messages.error(request,"email not found in our records")
        #     return render(request, 'registration/phone.html')
            
        return render(request, 'registration/phone.html')
    
    
class payment_rejected(View):
    def get(self, request):
        return render(request, 'dashboard/reject_payment.html')
    
    
    def post(self, request):
        return render(request, 'dashboard/reject_payment.html')
    
    
class Myemail(View):
    def get(self, request):
        emails = Profiles.objects.filter(status='pending')
        registerdemail = MyUser.objects.all()
        
        return render(request, 'email.html',{'emails':emails,'registerdemail':registerdemail})
    
    
    def post(self, request):
        return render(request, 'email.html')


#forget password here with email

class PasswordRest(View):
    def get(self, request):
        return render(request, 'registration/forget.html')

    def post(self, request):
        email = request.POST['email']
        users = MyUser.objects.filter(email=email)
        
        sitedomain =  get_current_site(request)
        subject = "Password Reset Request"
   
        if users.exists():
            content_email ={

                'user': users[0],
                'domain': sitedomain.domain,
                'uid':  urlsafe_base64_encode(force_bytes(users[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(users[0])
            }

            # html_message =  render_to_string(template_name='dashboard/forget_password.html', context=context)
            # myemaill = EmailMultiAlternatives(subject,body,EMAIL_HOST_USER, [emaildata] )
            # myemaill.attach_alternative(html_message, 'text/html')
            # myemaill.send()
           
            messages.success(request, 'email reset token has been sent to  your email')

            links = reverse('mypassword', kwargs={
                'uidb64':content_email['uid'], 'token':content_email['token']})
            links_urls = sitedomain.domain+links

            body = f"Hello, your password reset link is: \n Please click the link below or copy it to your browser \n,{links_urls}"
            send_mail(subject, body,EMAIL_HOST_USER, [email])
            messages.success(request, "The email has been sent with a link.  ")
            return render(request, 'registration/forget.html')

        
        else:
            messages.success(request, 'email not found on our database try again')
            return render(request, 'registration/forget.html')

class Set_NewPassword(View):
    def get(self, request, uidb64,token):
        user_id =  urlsafe_base64_decode(force_str(uidb64))
        users = MyUser.objects.get(pk=user_id)

        if not PasswordResetTokenGenerator().check_token(users,token):
            messages.error(request,'The password link has been used generate a new one ')
            return render(request, 'registration/forget.html')
           


        return render(request, 'registration/complete_password.html')
    
    
    def post(self,request,uidb64,token):
        password = request.POST['password']
        password2 = request.POST['password2']

        if len(password) < 6:
            messages.error(request,'password too short')
            return render(request, 'registration/complete_password.html')
        if password != password2:
            messages.error(request,'Password did not match')
            return render(request, 'registration/complete_password.html')
        
        user_id = urlsafe_base64_decode(force_str(uidb64))
        user = MyUser.objects.get(pk=user_id)
        user.set_password(password)
        mysave = user.save()
        messages.error(request,'Your Password set sucessfully')
        return redirect('complete')
       
        

        
        

class CompletePassword(View):
    def get(self, request):
        return render(request, 'registration/password_sucess.html')


    def post(self, request):
        return render(request, 'registration/password_sucess.html')
    

        
    
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profiles
from django.contrib import messages

# Create your views here.

User = get_user_model()

class Profile(LoginRequiredMixin,View):
    login_url = 'login'
    #LoginRequiredMixin,
    def get(self,request):
        # myprofile = Profiles.objects.filter(user=request.user)
        # if myprofile:
        #     return redirect()
        
        # myprofile = Profiles.objects.exists()
        # if myprofile:
        #     return redirect('dash')
            
            
        
        
        return render(request, 'index2.html')
    
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        state = request.POST['state']
        city = request.POST['city']
        local_govt = request.POST['local_govt']
        phone_number = request.POST['phone_number']
        contact = request.POST['contact']
        laptop = request.POST['laptop']
        certificate = request.POST['certificate']
        occupation =    request.POST['occupation']
        uplaod_picture   = request.FILES.get('file')
        sponsors =       request.POST['sponsors']
        
        Profiles.objects.create(first_name=first_name,last_name=last_name,state=state,
        city=city,local_govt=local_govt,phone_num=phone_number,contact_add=contact,sponsorship=sponsors,
        laptop=laptop,certifcate=certificate, occupation=occupation,uplaod_picture=uplaod_picture,user=request.user )
        messages.success(request, "profile created succesfully")
        return redirect('task')





    


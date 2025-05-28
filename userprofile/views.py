from django.http import JsonResponse
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
        if Profiles.objects.filter(user=request.user).exists():
            return redirect('/studenttask/task_collection')
    
            
            
        
        
        return render(request, 'index2.html')
    
    def post(self, request):
    # Check if profile already exists
        if Profiles.objects.filter(user=request.user).exists():
            return JsonResponse({'redirect_url': '/studenttask/task_collection'}, status=200)

        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        state = request.POST.get('state')
        city = request.POST.get('city')
        local_govt = request.POST.get('local_govt')
        phone_number = request.POST.get('phone_number')
        contact = request.POST.get('contact')
        laptop = request.POST.get('laptop')
        certificate = request.POST.get('certificate')
        occupation = request.POST.get('occupation')
        upload_picture = request.FILES.get('file')
        sponsors = request.POST.get('sponsors')

        # Create profile
        Profiles.objects.create(
            first_name=first_name,
            last_name=last_name,
            state=state,
            city=city,
            local_govt=local_govt,
            phone_num=phone_number,
            contact_add=contact,
            sponsorship=sponsors,
            laptop=laptop,
            certifcate=certificate,
            occupation=occupation,
            uplaod_picture=upload_picture,
            user=request.user,
        )

        return JsonResponse({'message': 'Profile created successfully'}, status=201)
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib  import messages
from django.http import JsonResponse
import json
from django.contrib import auth
from userprofile.models import Profiles
import pdb
import re
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login, logout
from projects.models import Task_collections


User = get_user_model()

# Create your views here.

# class Usernamevalidation(View):
#     def post(self,request):
        #loading the html data and converting it to  python dic
        # data = json.loads(request.body)
        #pick the username from the data
        # username = data['username']
        # if not str(username).isalnum():
        #     return JsonResponse({'username_error': 'username should only contain alphameric character'})
        # return JsonResponse({'username_valid': 'yes'})


# Updated User validation Code by:Da'Guy
def uservalidation(request):
    username = request.GET.get('username', '').strip()  # Trim spaces

    if not username:  # Check if username is missing or empty
        return JsonResponse({'error': 'Username parameter is required'}, status=400)

    is_taken = User.objects.filter(username=username).exists()

    data = {
        'is_taken': is_taken,
        'message': "Username is already taken" if is_taken else "Username is available"
    }

    return JsonResponse(data)


# Old Phone verification Code

# def phonevalidation(request):
#     phone = request.GET.get('phone', None)
#     data = {
#         'is_taken': User.objects.filter(phone=phone).exists()
        
#     }
#     return JsonResponse(data)


# New Phone verification Code by:Da'Guy
def phonevalidation(request):
    phone = request.GET.get('phone', '').strip()  # Remove extra spaces

    if not phone:  # Handle missing or empty phone number
        return JsonResponse({'error': 'Phone number parameter is required'}, status=400)

    # if not re.fullmatch(r'^\+?\d{7,15}$', phone):  # Validate phone format
    #     return JsonResponse({'error': 'Invalid phone number format'}, status=400)

    is_taken = User.objects.filter(phone=phone).exists()

    data = {
        'is_taken': is_taken,
        'message': "Phone number is already registered" if is_taken else "Phone number is available"
    }

    return JsonResponse(data)

        

# New Email verification Code by:Da'Guy
# Added rate limiting to prevent abuse 
@ratelimit(key='ip', rate='5/m', method='GET', block=True)  # Limit to 5 requests per minute per IP
def emailvalidation(request):
    email = request.GET.get('email', '').strip()  # Remove extra spaces

    if not email:  # Handle missing or empty email
        return JsonResponse({'error': 'Email parameter is required'}, status=400)

    # Validate email format using regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.fullmatch(email_regex, email):
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    is_taken = User.objects.filter(email=email).exists()

    data = {
        'is_taken': is_taken,
        'message': "Email is already registered" if is_taken else "Email is available"
    }

    return JsonResponse(data)

# New Phone verification Code by:Da'Guy
@ratelimit(key='ip', rate='5/m', method='GET', block=True)  # Limit to 5 requests per minute per IP
def phonevalidation(request):
    phone = request.GET.get('phone')
    data = {'is_taken': User.objects.filter(phone=phone).exists()}
    return JsonResponse(data)



    
    

class Registration(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # Get form data
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        username = request.POST.get('username')

        # Check for empty fields
        if not email or not phone or not password or not confirm_password or not username:
            return JsonResponse({'error': "All fields are required."}, status=400)

        # Password validation
        if password != confirm_password:
            return JsonResponse({ 'error': "Passwords do not match"}, status=400)
        if len(password) < 5:
            return JsonResponse({'error': "Password too short"}, status=400)

        # Check if user already exists
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'error': "Phone number already registered"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': "Email already registered"}, status=400)
        

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Username already taken"}, status=400)

        # Create user
        user = User.objects.create_user(email=email, username=username, phone=phone)
        user.set_password(password)
        user.save()

        return JsonResponse({'success': 'Registration Successfully ', 'redirect': '/reg/login'})



# Updated Login Code by:Da'Guy
class Login(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if not phone or not password:
            return JsonResponse({'error': 'Phone and password are required'}, status=400)

        if not User.objects.filter(phone=phone).exists():
            return JsonResponse({'error': 'Invalid phone number'}, status=400)

        user = auth.authenticate(phone=phone, password=password)
        if user:
            auth.login(request, user)
            
            if not Profiles.objects.filter(user=user).exists():
                return JsonResponse({
                    'profile': 'Complete Your Registration',
                    'redirect_url': '/profile'
                })
            has_any_tasks = Task_collections.objects.filter(student=user).exists()
            
            # if not has_any_tasks:
            #     return JsonResponse({
            #         'task': 'Please submit your first task',
            #         'redirect_url': '/cohorts/task_collection'
            #     })
            

            unapproved_tasks = Task_collections.objects.filter(
                student=user,
                status__in=['pending', 'rejected']
            ).exists()
            
            # if unapproved_tasks:
            #     return JsonResponse({
            #         'unapproved': 'You have unapproved tasks',
            #         'redirect_url': '/cohorts/task_collection'
            #     })
            return JsonResponse({'success': 'Login successful', 'redirect_url': '/dashboard/'})

        return JsonResponse({'error': 'Incorrect password'}, status=401)


class Logout(View):
    def get(self,request):
        auth.logout(request)
        messages.success(request,'logout successfully')
        return redirect('login')
# from django.shortcuts import render, redirect
# from django.views.generic import View
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# import pdb
# from userprofile.models import Profiles
# from cohorts.models import Livesesion
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from portal.settings import EMAIL_HOST_USER
# from projects .models import Assigment, Project
# # Create your views here.


# class MyCourses(LoginRequiredMixin,View):
#     login_url = 'login'
    
#     def get(self,request):

#         try:
#             assign = Assigment.objects.get(user=request.user)
#             if assign.score_project < 15:
#                 return  redirect('reating')
#         except: assign = None
        
        
        
        
#         try:
#             adimission = Profiles.objects.get(user=request.user)
#         except:   adimission =  None
        
#         try:
#           assigment = Payment.objects.get(user=request.user)
#         except: assigment = None
        
#         front_end = Courses.objects.filter(material__name='Front-end-materials')
      
#         html5 =  Courses.objects.get(material__pk=3)
#         css5 =  Courses.objects.get(material__pk=4)
#         boostrap =  Courses.objects.get(material__pk=5)
#         Javascripts =  Courses.objects.get(material__pk=6)
#         python3 =  Courses.objects.get(material__pk=7)
#         mysql =  Courses.objects.get(material__pk=9)
#         github = Courses.objects.get(material__pk=10)
#         mydjango  =  Courses.objects.get(material__pk=8)
#         product_design = Courses.objects.get(material__pk=11)
#         # mydjango  =  Courses.objects.get(material__pk=9)
        
#         my_back = Courses.objects.filter(material__name='Back-end-materials')
#         total_payment = Payment.total_amount(request.user)
#         context = {
            
#             'mysql':mysql, 
#             'my_back':my_back,
#             'adimission':adimission,
#             'assigment': assigment,
#              "github":  github,
#              'python3':python3,
#              'Javascripts':Javascripts,
#              'boostrap':boostrap,
#              'css5':css5,
#             'html5':html5,
#             'reactjs': mydjango,
#             'total_payment':total_payment,
#             'product_design':product_design

#         }
#         return render(request, 'dashboard/training_materials.html',context=context)
    
    
#     def post(self,request):
#         return render(request, 'dashboard/training_materials.html')


# class Materialspayment(LoginRequiredMixin,View):
#     login_url = 'login'
#     def get(self, request):
        
    
#         total_payment = Payment.total_amount(request.user)
       
#         try:
#             payments= Payment.objects.get(user=request.user)
#         except:   payments =  None
        
#         try:
#             adimission = Profiles.objects.get(user=request.user)
#         except:   adimission =  None
#         context = {
#             'payment':payments,
#             'adimission':adimission,
#             'total_payment': total_payment
            
            
            
#         }
        
#         return render(request, "dashboard/payment.html",context=context)
    
#     def post(self, request):
#         materials = request.POST['materials']
#         amount_paid = request.POST['amount_paid']
#         date  =      request.POST['date']
#         payment_type = request.POST['payment_type']
#         payment_file = request.FILES.get('myfiles')
#         if not amount_paid :
#             messages.error(request, 'fill all the form before submitting')
#             return render(request, "dashboard/payment.html")
        
    
       
#         mypayment = Payment.objects.create( user=request.user,amount=amount_paid,courses=materials, 
#                    payment_type=payment_type, date=date,uplaod=payment_file)
#         mypayment.mysave()
        
#         mypayment.save()
#         messages.success(request, 'payment for material submit successfully, refresh the page to generate payment reciept')
#         return redirect('gen')
    

# class UpdateMaterials(LoginRequiredMixin,View):
#     login_url = 'login'
#     def get(self, request, pk):
        
    
#         total_payment = Payment.total_amount(request.user)
       
#         try:
#             payments= Payment.objects.get(user=request.user)
#         except:   payments =  None
        
      
        
#         try:
#             adimission = Profiles.objects.get(user=request.user)
#         except:   adimission =  None
#         context = {
#             'payment':payments,
#             'adimission':adimission,
#             'total_payment': total_payment
            
            
#         }
        
#         return render(request, "dashboard/payment_update.html",context=context)
    
#     def post(self, request, pk):
#         updated = Payment.objects.get(pk=pk)
      
#         date  =      request.POST['date']
#         amount  =      request.POST['paid']
#         payment_file = request.FILES.get('myfiles')
#         myamount = updated.amount + int(amount)
        
#         updated.amount = myamount
#         updated.uplaod = payment_file
#         updated.date =  date
#         updated.save()
#         messages.success(request, 'payment for material submit successfully, refresh the page to generate payment reciept')
#         return redirect('payment')
        
    

# class Paymentslips(View):
#     def get(self, request):
#         try:
           
#             payments= Payment.objects.get(user=request.user)
           
#         except:   payments =  None
#         return render(request, 'dashboard/slips.html',{'payment':payments})
    
    
#     def post(self, request):
#         return render(request, 'dashboard/slips.html')
    

# class Gen(View):
#     def get(self,request):
#         return render(request, 'dashboard/gen.html')
    
    
#     def post(self,request):
#         return render(request, 'dashboard/gen.html')
        

# class Edit_Liveclass(View):
#     def get(self,request, pk):
#         mylive = Livesesion.objects.get(pk=pk)
#         online = Livesesion.objects.all()

#         return render(request, 'dashboard/edit_liveclass.html', {'mylive':mylive, 'online':online})
            
    
#     def post(self,request, pk):
#         title  = request.POST['title']
#         myurl  = request.POST['url']
#         date =  request.POST['date']
#         mystatus  =   request.POST['class_status']
#         mylive = Livesesion.objects.get(pk=pk)
#         mylive.title = title
#         mylive.link = myurl
#         mylive.online = mystatus
#         mylive.date = date
#         mylive.save()
#         admitted = Profiles.objects.filter(status='admitted')
#         subject = "Link for class is now avaliable"
#         from_email = EMAIL_HOST_USER
#         text = "Welcome "
#         current_site = get_current_site(request)
#         context = {
#             "mylive":mylive,
        
        
#         'current_site':   current_site}
#         html_message = render_to_string(
#                     template_name='dashboard/class_link.html', context=context)
       
#         for admit in admitted:
#             toemail = admit.user.email
#             mysend = EmailMultiAlternatives( subject, text, from_email, [toemail])
#             mysend.attach_alternative(html_message, 'text/html')
#             mysend.send()
#             messages.success(request, 'update class sucessfully')
#             # pdb.set_trace()
#         return render(request, 'dashboard/edit_liveclass.html')
    
    
   
from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class Homepage(View):
    def get(self,request):
        return render(request, 'home/index.html')
    
    
    def post(self,request):
        return render(request, 'home/index.html')
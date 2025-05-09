from django.shortcuts import render
from django.views.generic import View
from .models import Ebooks
from django.http import HttpResponse


# Create your views here.

def html5(request):
    document = Ebooks.objects.get(pk=4)
    with open(document.ebook_files.path, 'rb') as files:
         #This tells browsers that the document is a pdf file, not of HTML file.
        res = HttpResponse(files.read(), content_type='application/pdf')
         #this  code get the filename and downloads files with that name.
        res['content-Dispostion'] = f'attachement; filename="{document.name}"'
        return res


def css5(request):
    cssfiles = Ebooks.objects.get(pk=5)
    with open(cssfiles.ebook_files.path, 'rb') as files:
         #This tells browsers that the document is a pdf file, not of HTML file.
        css = HttpResponse(files.read(), content_type='application/pdf')
         #this  code get the filename and downloads files with that name.
        css['content-Dispostion'] = f'attachement; filename="{cssfiles.name}"'
        return css




def prdouct(request):
    cssfiles = Ebooks.objects.get(pk=6)
    with open(cssfiles.ebook_files.path, 'rb') as files:
         #This tells browsers that the document is a pdf file, not of HTML file.
        css = HttpResponse(files.read(), content_type='application/pdf')
         #this  code get the filename and downloads files with that name.
        css['content-Dispostion'] = f'attachement; filename="{cssfiles.name}"'
        return css
# def django(request):
#     document = Ebooks.objects.get(pk=3)
#     with open(document.ebook_files.path, 'rb') as files:
#          #This tells browsers that the document is a pdf file, not of HTML file.
#         res = HttpResponse(files.read(), content_type='application/pdf')
#          #this  code get the filename and downloads files with that name.
#         res['content-Dispostion'] = f'attachement; filename="{document.name}"'
#         return res
    
  
        
        
    


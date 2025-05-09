from django.db import models

# Create your models here.

class Ebooks(models.Model):
    name = models.CharField(max_length=200)
    ebook_files = models.FileField(upload_to='ebooks')
    created_at  = models.DateField(auto_now_add=True)

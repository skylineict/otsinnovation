from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField



User = get_user_model()

class Task(models.Model):
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='abcdefghijklmnqszxcvopl1234567890')
    task   = models.CharField(max_length=200)
    task_img = models.ImageField(upload_to='taskimage')
    links =  models.URLField()
    task_description = RichTextUploadingField(blank=True)
    
    
    def __str__(self):
        return self.task



class Task_collections(models.Model):
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='abcdefghijklmnqszxcvopl1234567890')
    task_status = (
        ('pending', 'pending'),
        ('complete', 'complete')
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task   = models.CharField(max_length=500)
    status  = models.CharField(choices=task_status, max_length=200)
    screen_short= models.ImageField(upload_to='taskimage', ) 
    links =   models.URLField(blank=True)
    # links2  =  models.URLField(blank=True)
    # links3  =  models.URLField(blank=True)
    
    def __str__(self):
        return str(self.task)

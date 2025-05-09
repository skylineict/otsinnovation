from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from dash.models import Payment, Cohorts
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField


User = get_user_model()




class Project(models.Model):
    mystatus = (
        ('expired', 'expired'),
        ('active', 'active'),
        ('pending', 'pending')
    )
    
    project_name = models.CharField(max_length=200)
    ending_date = models.DateField(auto_created=True,blank=True, null=True)
    start_date = models.DateField(auto_created=True,blank=True, null=True)
    cohorts =   models.ForeignKey(Cohorts, on_delete=models.CASCADE, blank=True, null=True)
    status =    models.CharField(max_length=200, choices=mystatus, default='pending')
    descriptions = RichTextUploadingField(blank=True)
    
    
    def __str__(self):
        return self.project_name
    
    



class Assigment(models.Model):
    assigment = (
        ('reviewing', 'reviewing'),
        ('complete', 'complete'),
        ('reject', 'reject')
    )
    
    git_hub = models.CharField(max_length=100)
    user =   models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.CharField(max_length=10000)
    cohorts =  models.ForeignKey(Cohorts, on_delete=models.CASCADE)
    date  =   models.DateField(auto_now_add=True)
    passcode = models.CharField(max_length=200)
    status  = models.CharField(max_length=200, choices=assigment,default='reviewing')
    score_project  = models.IntegerField(default=1)

    def score_caculations(student):
        scores = Assigment.objects.filter(user=student)
        total_scores  = sum(myscore.score_project for myscore in scores )
        return total_scores
    
    
    def __str__(self):
        return self.project
    
    
# class Score(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     my_assigment =models.ForeignKey(Assigment, on_delete=models.CASCADE)
#     score  = models.IntegerField()
#     date  =  models.DateField(auto_now_add=True)
    
#     def __str__(self):
#         return str(self.score)
    
#     def score_caculations(student):
#         scores = Score.objects.filter(student=student)
#         total_scores  = sum(myscore.score for myscore in scores )
#         return total_scores

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

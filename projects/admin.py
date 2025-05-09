from django.contrib import admin
from .models import Project, Assigment, Task,Task_collections
# Register your models here.
@admin.register(Project)
class Student_Project(admin.ModelAdmin):
    list_display = ('project_name','cohorts','ending_date','start_date','descriptions', 'status')

@admin.register(Assigment)
class Myassigment(admin.ModelAdmin):
    list_display = ('git_hub','user', 'project', 'cohorts','date','score_project','status')
    

@admin.register(Task)
class Task_admin(admin.ModelAdmin):
    list_display = ('task', 'task_img','links','task_description')
    
    
@admin.register(Task_collections)
class Task_collect(admin.ModelAdmin):
    list_display = ('student','task', 'status', 'screen_short','links')
 
   
    
# @admin.register(Score)
# class Score_Admin(admin.ModelAdmin):
#     list_display = ('student','my_assigment', 'score')
    
    

     
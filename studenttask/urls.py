from django.urls import path

from .submit_task import Taskscollection
from .create_usertask import CreateTaskView




urlpatterns = [
    
   
    path('task_collection',Taskscollection.as_view(), name='task_collwction'),
    path('admintask',CreateTaskView.as_view(), name='createtask')
   
]

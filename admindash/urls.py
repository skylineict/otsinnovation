from django.urls import path
from .views import   DashAdmin, approved, approved_admission,Pending_student,approved_myproject,payment_reject,rejectassigment
from .create_usertask import CreateTaskView



urlpatterns = [
    path('', DashAdmin.as_view(), name='dash'),
    path('approved/<int:pk>',approved, name='myapproved'),
    path('approved_admission/<int:pk>',approved_admission, name='admission'),
    path('pending_approval/',Pending_student.as_view(), name='pending'),
    path('approved_admin/<int:pk>',approved_myproject, name='aproved_admin'),
    path('payment_decline/<int:pk>',payment_reject, name='payment_reject'),
    
    
    path('assignreject/<int:pk>',rejectassigment, name='assigmentrejected'),

    path('createtask',CreateTaskView.as_view(), name='createtask')

   
   
    # path('passcode', Passcode.as_view(), name='passcode')
    
]

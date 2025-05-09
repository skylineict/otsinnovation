from django.urls import path
from .views import Projects, Projects_datials, Payment_approval,view_payment,Submitassigment, Assigment_approval,Pending_payment,Create_Projects,Approve_project, Task_approval,approved_task,Payment_jected, RatingScore, Task_collections

from dash.views import myapproved


urlpatterns = [

    path('',Projects.as_view(), name='projects'),
    path('project/<int:pk>', Projects_datials.as_view(),name='project_datials'),
    path("pending_payment/",Payment_approval.as_view(), name="payment_approval" ),
     path("payment_approval/",Pending_payment.as_view(), name="pending_payment" ),
    path('view/<int:pk>', view_payment.as_view(),name='view_payment'),
    path('submitassigment', Submitassigment.as_view(),name='submitassigment'),
    path('assigment_approval', Assigment_approval.as_view(),name='assigment_approval'),
    path('create_project', Create_Projects.as_view(),name='add_project'),
    path('approve_project', Approve_project.as_view(),name='approval_project'),
    path('approved/<int:pk>',myapproved, name='assigment_approved'),
    path('task_approval', Task_approval.as_view(), name='task_me'),
    path('task_approved/<int:pk>',approved_task, name='task_appro' ),
    path("rejected_payment/",Payment_jected.as_view(), name="payment_rejected" ),
    path("rating/",RatingScore.as_view(), name="reating" ),
]

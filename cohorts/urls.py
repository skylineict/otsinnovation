from django.urls import path
from .views import Groupscohort, AllCohorts,Classroom,Recapclassroom,Tasks,Ourcommunity,Profileviews,Social_Profile,Profieupdate
from .submit_task import Taskscollection




urlpatterns = [
    
    path('mycohorts/<int:pk>',Groupscohort.as_view(), name='cohorts'),
    path('profileview/<slug:pk>',Profileviews.as_view(),name='profileview'),
    path('allcohorts/',AllCohorts.as_view(), name='groupscohort'),
    path('live/',Classroom.as_view(), name='live'),
    path('recap/',Recapclassroom.as_view(), name='recap'),
    path('task/',Tasks.as_view(), name='task'),
    path('task_collection/',Taskscollection.as_view(), name='task_collwction'),
    path('team/',Ourcommunity.as_view(), name='team'),
    path('socail/', Social_Profile.as_view(), name='social'),
    path('edit_profile/<slug:pk>',Profieupdate.as_view(),name='update_profile')
    
]

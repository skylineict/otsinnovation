from django.urls import path
from .views import   DashAdmin,Pending_student
from .classroom import AdminLiveclassView
from .course_registration_approval import CourseRegistrationApprovalView
from .search_couses import UserSearchApprovalView
from .filterby_course import FilterByCourseView, list_courses





urlpatterns = [
    path('', DashAdmin.as_view(), name='dash'),

    path('pending_approval/',Pending_student.as_view(), name='pending'),
    path('classroom',AdminLiveclassView.as_view(), name='classroom'),
     path('registrations/approve/', CourseRegistrationApprovalView.as_view(), name='approve_registrations'),
     path('registrations/search-approve/', UserSearchApprovalView.as_view(), name='user_search_approval'),

    path('registrations/filter-by-course/', FilterByCourseView.as_view(), name='filter_by_course'),
    path('listcourses/', list_courses, name='list_courses'),

    

  

   
   
   
    # path('passcode', Passcode.as_view(), name='passcode')
    
]

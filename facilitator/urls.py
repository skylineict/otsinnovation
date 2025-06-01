from django.urls import path
from .registration  import FacilitatorRegistrationView
from .facilitator_approval import FacilitatorApprovalView
from .student_list import FacilitatorStudentsView


urlpatterns = [
    path('', FacilitatorRegistrationView.as_view(), name='request_facilitator'),
    path('facilitator_approval', FacilitatorApprovalView.as_view(), name='facilitator_approval'),
      path('student_list', FacilitatorStudentsView.as_view(), name='student_list'),
 
    
]





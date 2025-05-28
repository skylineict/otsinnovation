from django.urls import path
from .registration  import FacilitatorRegistrationView
from .facilitator_approval import FacilitatorApprovalView


urlpatterns = [
    path('', FacilitatorRegistrationView.as_view(), name='request_facilitator'),
    path('facilitator_approval', FacilitatorApprovalView.as_view(), name='facilitator_approval'),
 
    
]





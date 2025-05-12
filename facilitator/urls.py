from django.urls import path
from .views import (
    RequestFacilitatorView,
    FacilitatorDashboardView,
    ManageFacilitatorRequestsView,
    ManageFacilitatorRequestView,
    FacilitatorStudentsView,
    ViewCourseFacilitatorView,
    FacilitatorStatsView,
    UpdateFacilitatorProfileView,
    GetFacilitatorInfoView,
)

urlpatterns = [
    path('', RequestFacilitatorView.as_view(), name='request_facilitator'),
    path('facilitator/', FacilitatorDashboardView.as_view(), name='facilitator_dashboard'),
    path('admin/facilitator/requests/', ManageFacilitatorRequestsView.as_view(), name='manage_facilitator_requests'),
    path('admin/facilitator/requests/<int:request_id>/manage/', ManageFacilitatorRequestView.as_view(), name='manage_facilitator_request'),
    path('facilitator/students/', FacilitatorStudentsView.as_view(), name='facilitator_students'),
    path('course/<int:course_id>/facilitator/', ViewCourseFacilitatorView.as_view(), name='view_course_facilitator'),
    path('facilitator/stats/', FacilitatorStatsView.as_view(), name='facilitator_stats'),
    path('facilitator/profile/update/', UpdateFacilitatorProfileView.as_view(), name='update_facilitator_profile'),
    path('course/<int:course_id>/facilitator/info/', GetFacilitatorInfoView.as_view(), name='get_facilitator_info'),
]
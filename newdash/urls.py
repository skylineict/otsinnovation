from django.urls import path
from . import views
from .views import  flutterwave_webhook, payment_success


urlpatterns = [
    # Course Registration
   

    # Flutterwave Payment
    path('webhook/flutterwave/', flutterwave_webhook, name='flutterwave_webhook'),
    path('payment_success', payment_success, name='payment_success'),

    # Facilitator URLs
    path('become-facilitator/', views.request_facilitator, name='request_facilitator'),
    path('facilitator/dashboard/', views.facilitator_dashboard, name='facilitator_dashboard'),
    path('facilitator/students/', views.facilitator_students, name='facilitator_students'),
    path('facilitator/stats/', views.facilitator_stats, name='facilitator_stats'),
    path('facilitator/profile/', views.update_facilitator_profile, name='update_facilitator_profile'),

    # Admin URLs for managing facilitators
    path('admin/facilitators/', views.manage_facilitator_requests, name='manage_facilitator_requests'),
    path('admin/facilitators/approve/<int:request_id>/', views.approve_facilitator_request, name='approve_facilitator_request'),
    path('admin/facilitators/reject/<int:request_id>/', views.reject_facilitator_request, name='reject_facilitator_request'),

    # Student Viewing Course Facilitator
    path('course/<int:course_id>/facilitator/', views.view_course_facilitator, name='view_course_facilitator'),

    # API endpoints
    path('api/facilitator-info/<int:course_id>/', views.get_facilitator_info, name='get_facilitator_info'),
]

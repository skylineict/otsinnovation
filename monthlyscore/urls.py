from django.urls import path
from .views import CourseListAPIView, MonthlyRequirementView
from .monthlyscoreapproval import ApproveMonthlyRequirementView


urlpatterns = [
    path('api/courses/', CourseListAPIView.as_view(), name='course_list_api'),
    path('monthly-requirement/', MonthlyRequirementView.as_view(), name='monthly_requirement'),
    path('approve-requirement/', ApproveMonthlyRequirementView.as_view(), name='approve_requirement'),
]
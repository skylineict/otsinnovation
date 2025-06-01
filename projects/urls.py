from django.urls import path
from .create_project import ProjectVeiw





urlpatterns = [
    path('', ProjectVeiw.as_view(), name='create_project'),


]


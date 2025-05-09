from django.forms import  ModelForm
from .models import Project, Task

class bodyform(ModelForm):
    class Meta:
        model = Project
        fields = ["descriptions"]
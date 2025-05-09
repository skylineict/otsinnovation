from django.db import models


#creating email sending application to all applicants

class Messages(models.Model):
    subjects  = models.CharField(max_length=400)
    message = models.TextField(max_length=1000)
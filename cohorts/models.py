from django.db import models
from venv import logger
from django.db import IntegrityError, models
from registration.models import MyUser
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from django.core.exceptions import ValidationError
import pyotp
import base64
import os
from courses.models import Course

# Create your models here.


# New Cohort Model
class Cohort(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cohort', null=True, blank=True)
    leader = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_cohorts')
    students = models.ManyToManyField(MyUser, related_name='cohorts')
    whatsapp_link = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.students.count() > 20:
            raise ValidationError("Cohort cannot have more than 20 students")

    def __str__(self):
        return f"{self.name} ({self.course.name})"

# NEW: Model to track cohort leader nominations
class CohortLeaderNomination(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='leader_nominations')
    nominator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='nominations_made')
    nominee = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='nominations_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    nomination_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.nominee not in self.cohort.students.all():
            raise ValidationError("Nominee must be a member of the cohort")
        if self.cohort.leader:
            raise ValidationError("Cohort already has a leader")
        if not (self.nominator in self.cohort.students.all() or 
                Course.objects.filter(facilitators=self.nominator, id=self.cohort.course.id).exists() or 
                self.nominator.is_superuser):
            raise ValidationError("Nominator must be a cohort member, facilitator, or superuser")

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.status == 'pending' and self.cohort.course.facilitators:
    #         send_mail(
    #             subject=f"New Cohort Leader Nomination for {self.cohort.name}",
    #             message=f"{self.nominator.username} nominated {self.nominee.username} as leader for {self.cohort.name}. Reason: {self.nomination_reason or 'None'}",
    #             from_email=settings.DEFAULT_FROM_EMAIL,
    #             recipient_list=[self.cohort.course.facilitators.email],
    #             fail_silently=True,
    #         )

    class Meta:
        unique_together = ('cohort', 'nominee')

    def __str__(self):
        return f"Nomination of {self.nominee.username} for {self.cohort.name}"


class Recapcourse(models.Model):
    name = models.CharField(max_length=200, default=1)
    
    def __str__(self):
        return self.name
    
class Recapsesion(models.Model):
    title = models.CharField(max_length=200)
    link    = models.URLField(max_length=300)
    date  =  models.DateField(auto_created=True)
    image =  models.ImageField(upload_to='sesion')
    courses  =  models.ForeignKey(Recapcourse, on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return self.title


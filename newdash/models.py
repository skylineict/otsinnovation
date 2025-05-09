from django.db import models
from registration.models import MyUser
from django.contrib.auth.models import AbstractUser
from django import forms
from registration.models import MyUser
from django.contrib.auth import get_user_model
from  courses.models import Course
from shortuuid.django_fields import ShortUUIDField

from django.utils import timezone






class FacilitatorRegistration(models.Model):
    id = ShortUUIDField(
        primary_key=True, 
        unique=True, 
        editable=False, 
        alphabet='abcdefghijklmnqszxcvopl1234567890')
    # Changed from OneToOneField to ForeignKey to allow multiple applications
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='facilitator_requests')
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    internship_available = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if the facilitator is approved and the course doesn't already have a facilitator
        if self.approved and self.course.facilitators is None:
            self.course.facilitators = self.user  # Assign the user as the facilitator
            self.course.save()  # Save the course with the new facilitator
        super().save(*args, **kwargs)  # Proceed with saving the facilitator registration

    def __str__(self):
        return f"{self.user.username} for {self.course.name}"
 # Add a unique constraint to ensure user can only apply once per course
    class Meta:
        unique_together = ('user', 'course')
class MyUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    linkedin_profile = models.URLField(blank=True, null=True)
    twitter_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)

    @property
    def social_media(self):
        return {
            'linkedin': self.linkedin_profile,
            'twitter': self.twitter_profile,
            'github': self.github_profile
        }


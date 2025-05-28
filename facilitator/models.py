
from django.db import models
from django.contrib.auth import get_user_model
from  courses.models import Course
from shortuuid.django_fields import ShortUUIDField
from courses.models import Course
from courses.models import CourseRegistration
from registration.models import MyUser
from django.utils import timezone  # ✅







# FacilitatorRegistration Model (UNCHANGED)
class FacilitatorRegistration(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='facilitator_requests')
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)
    rejection_timestamp = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.course.facilitators and not self.approved:
            self.approved = False
            self.rejection_reason = "Course already has an approved facilitator."
            self.rejection_timestamp = timezone.now()
            super().save(*args, **kwargs)
            # send_mail(
            #     subject="Facilitator Application Rejected",
            #     message=f"Your application to facilitate {self.course.name} has been rejected because the course already has an approved facilitator.",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[self.user.email],
            #     fail_silently=True,
            # )
        else:
            if self.approved and self.course.facilitators is None:
                self.course.facilitators = self.user
                self.course.save()
                # send_mail(
                #     subject="Facilitator Application Approved",
                #     message=f"Congratulations! Your application to facilitate {self.course.name} has been approved.",
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     recipient_list=[self.user.email],
                #     fail_silently=True,
                # )
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} for {self.course.name}"

    class Meta:
        unique_together = ('user', 'course')




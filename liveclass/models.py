from datetime import timezone
from decimal import Decimal
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField
from courses.models import Course
from courses.models import CourseRegistration
from registration.models import MyUser
from monthlyscore.models import StudentPoint

# LiveClass Model
# LiveClass Model (UNCHANGED)
class LiveClass(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    ]
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_classes')
    facilitator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='live_classes')
    topic = models.CharField(max_length=255)
    image = models.ImageField(upload_to='live_class_images/', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    join_link = models.URLField()
    attendance_points = models.PositiveIntegerField(default=0)
    enable_attendance = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")

    def update_status(self):
        now = timezone.now()
        if now < self.start_time:
            self.status = 'upcoming'
        elif self.start_time <= now <= self.end_time:
            self.status = 'live'
        else:
            self.status = 'finished'
            self.enable_attendance = False
        self.save()

    def save(self, *args, **kwargs):
        # MODIFIED: Only notify non-suspended students
        super().save(*args, **kwargs)
        if self.status == 'upcoming':
            students = CourseRegistration.objects.filter(course=self.course, is_approved=True, account_suspended=False)
            recipient_list = [reg.user.email for reg in students if reg.user]
            # send_mail(
            #     subject=f"New Live Class Scheduled: {self.topic}",
            #     message=f"A new live class '{self.topic}' is scheduled for {self.start_time}. Join link: {self.join_link}",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=recipient_list,
            #     fail_silently=True,
            # )

    def __str__(self):
        return f"{self.topic} ({self.course.name})"


# LiveClassAttendance Model
class LiveClassAttendance(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='class_attendances')
    timestamp = models.DateTimeField(auto_now_add=True)
    points_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('live_class', 'student')

    # MODIFIED: Added check for suspended students
    def save(self, *args, **kwargs):
        registration = CourseRegistration.objects.filter(user=self.student, course=self.live_class.course).first()
        if registration and registration.account_suspended:
            raise ValidationError("Suspended students cannot mark attendance")
        if self.live_class.status != 'live' or not self.live_class.enable_attendance:
            raise ValidationError("Attendance cannot be marked for this class")
        if not self.points_awarded:
            self.points_awarded = self.live_class.attendance_points
        super().save(*args, **kwargs)
        if registration:
            registration.reward_points += self.points_awarded
            registration.save()
        student_point, created = StudentPoint.objects.get_or_create(
            user=self.student,
            course=self.live_class.course,
            defaults={'total_points': self.points_awarded}
        )
        if not created:
            student_point.total_points += self.points_awarded
            student_point.save()
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms import ValidationError

from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField
from courses.models import Course
from datetime import timezone
from decimal import Decimal
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField
from courses.models import Course
from courses.models import CourseRegistration
from cohorts.models import Cohort


User = get_user_model()

#  Project Model (UNCHANGED)
class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('cohort', 'Cohort'),
    ]
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('finished', 'Finished'),
    ]
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    deadline = models.DateTimeField()
    max_score = models.PositiveIntegerField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    cohorts = models.ManyToManyField(Cohort, related_name='projects', blank=True)
    file = models.FileField(upload_to='project_files/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.project_type == 'cohort' and not self.cohorts.exists():
            raise ValidationError("Cohort projects must be assigned to at least one cohort")

    @property
    def current_status(self):
        if self.deadline < timezone.now():
            return 'finished'
        return self.status

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now():
            self.status = 'finished'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.course.name})"

# ProjectSubmission Model
class ProjectSubmission(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_submissions')
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, null=True, blank=True, related_name='submissions')
    file = models.FileField(upload_to='project_submissions/',null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)

    # MODIFIED: Added check for suspended students
    def clean(self):
        registration = CourseRegistration.objects.filter(user=self.submitted_by, course=self.project.course).first()
        if registration and registration.account_suspended:
            raise ValidationError("Suspended students cannot submit projects")
        if self.project.current_status == 'finished':
            raise ValidationError("Cannot submit to a finished project")
        if self.project.project_type == 'individual':
            if self.cohort:
                raise ValidationError("Individual projects cannot have a cohort")
            if not CourseRegistration.objects.filter(user=self.submitted_by, course=self.project.course, is_approved=True).exists():
                raise ValidationError("Submitter must be a registered student for the course")
        elif self.project.project_type == 'cohort':
            if not self.cohort:
                raise ValidationError("Cohort must be specified for cohort projects")
            if self.submitted_by != self.cohort.leader:
                raise ValidationError("Only cohort leader can submit cohort projects")
            if self.cohort not in self.project.cohorts.all():
                raise ValidationError("Cohort must be one of the project's assigned cohorts")

    def __str__(self):
        return f"Submission for {self.project.title} by {self.submitted_by.username}"

# ProjectAttendance Model
class ProjectAttendance(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    submission = models.ForeignKey(ProjectSubmission, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_attendances')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('submission', 'student')

    # MODIFIED: Added check for suspended students
    def save(self, *args, **kwargs):
        registration = CourseRegistration.objects.filter(user=self.student, course=self.submission.project.course).first()
        if registration and registration.account_suspended:
            raise ValidationError("Suspended students cannot participate in cohort projects")
        if self.submission.project.project_type != 'cohort':
            raise ValidationError("Attendance is only for cohort projects")
        if self.student not in self.submission.cohort.students.all():
            raise ValidationError("Student is not in the cohort")
        super().save(*args, **kwargs)
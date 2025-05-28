from datetime import timezone
from decimal import Decimal
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from shortuuid.django_fields import ShortUUIDField
from courses.models import Course,SuspensionFine
from courses.models import CourseRegistration
from projects.models import Project,ProjectSubmission,ProjectAttendance


User = get_user_model()


# CourseMonthlyRequirement Model
class CourseMonthlyRequirement(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='monthly_requirements')
    month = models.DateField()
    score_requirement = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'month')

    def __str__(self):
        return f"{self.course.name} - {self.month.strftime('%B %Y')} Requirement: {self.score_requirement}"

# ComplianceRecord Model
class ComplianceRecord(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE, related_name='compliance_records')
    month = models.DateField()
    total_score = models.PositiveIntegerField(default=0)
    is_compliant = models.BooleanField(default=False)
    warning_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_compliance(self):
        start_date = self.month  
        end_date = (start_date + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(seconds=1)  # Last 
        submissions = ProjectSubmission.objects.filter(
        project__course=self.registration.course,
            submitted_at__range=(start_date, end_date),
            is_approved=True
    )

        total_score = 0  
        for sub in submissions:
            if sub.project.project_type == 'individual' and sub.submitted_by == self.registration.user:
                total_score += sub.score or 0  # Add their score
            elif sub.project.project_type == 'cohort' and sub.cohort and self.registration.user in sub.cohort.students.all():
               
                if ProjectAttendance.objects.filter(submission=sub, student=self.registration.user).exists():
                    attendance_count = sub.attendances.count()  
                    if attendance_count > 0:
                        total_score += (sub.score or 0) // attendance_count

       
        self.total_score = total_score
        monthly_requirement = CourseMonthlyRequirement.objects.filter(
            course=self.registration.course,
            month=self.month
        ).first()

        
        if monthly_requirement:
            self.is_compliant = self.total_score >= (monthly_requirement.score_requirement * Decimal('0.5'))
        else:
            self.is_compliant = False  # No requirement found means treat as non-compliant

        self.save() 
        if self.is_compliant:
            return
        previous_failures = ComplianceRecord.objects.filter(
            registration=self.registration,
            is_compliant=False,
            warning_sent=True  # Indicates they were already warned
        ).exclude(id=self.id)
        if previous_failures.exists():
            self.registration.account_suspended = True
            self.registration.suspension_reason = (
                f"Your account has been suspended due to repeated non-compliance. "
                f"You failed to meet 50% of the required score for {self.month.strftime('%B %Y')}."
            )
            self.registration.save()

            # Add or create a fine (e.g., ₦50.00) for suspension
            SuspensionFine.objects.get_or_create(
                registration=self.registration,
                defaults={'amount': Decimal('50.00')}
            )

            # Send a suspension email to the user
            # send_mail(
            #     subject=f"Account Suspended for {self.month.strftime('%B %Y')}",
            #     message=(
            #         f"Dear {self.registration.full_name},\n\n"
            #         f"You have failed to meet the required score again for the course "
            #         f"'{self.registration.course.name}' in {self.month.strftime('%B %Y')}.\n"
            #         f"As this is your second failure, your account has now been suspended.\n\n"
            #         f"A fine of ₦50.00 has been applied. Please visit your dashboard to pay and request reinstatement.\n\n"
            #         f"Thank you,\nTraining Team"
            #     ),
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[self.registration.user.email],
            #     fail_silently=False,
            # )

        # 10. If this is their first failure and no warning has been sent before
        elif not self.warning_sent:
            # Send only a warning and mark warning_sent = True
            self.warning_sent = True
            self.save()

            # # Send a warning email to the student
            # send_mail(
            #     subject=f"Warning: Low Monthly Score for {self.month.strftime('%B %Y')}",
            #     message=(
            #         f"Dear {self.registration.full_name},\n\n"
            #         f"You did not meet the minimum score requirement for the course "
            #         f"'{self.registration.course.name}' in {self.month.strftime('%B %Y')}.\n\n"
            #         f"Required Score: {monthly_requirement.score_requirement}\n"
            #         f"Your Score: {self.total_score}\n\n"
            #         f"This is a warning. If you fail to meet the requirement again next month, your account will be suspended.\n\n"
            #         f"Thank you,\nTraining Team"
            #     ),
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[self.registration.user.email],
            #     fail_silently=False,
            # )


    class Meta:
        unique_together = ('registration', 'month')

    def __str__(self):
        return f"Compliance for {self.registration.full_name} - {self.month.strftime('%B %Y')}"
    


# StudentPoint Model (UNCHANGED)
class StudentPoint(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_points')
    total_points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.name}: {self.total_points} points"
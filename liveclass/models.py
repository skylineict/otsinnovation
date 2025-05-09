from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from registration import models, myusermanager
import uuid

# Model for courses
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    facilitators = models.ManyToManyField(User, related_name='courses_teaching')
    students = models.ManyToManyField(User, related_name='courses_enrolled', through='CourseEnrollment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']

# Model for live class enrollment

class LiveClass(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_classes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    facilitator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facilitated_classes')
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    meeting_link = models.URLField(blank=True, null=True)
    meeting_id = models.CharField(max_length=100, blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True, null=True)
    join_code = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # New field to control attendance marking
    attendance_active = models.BooleanField(default=False)
    attendance_activated_at = models.DateTimeField(null=True, blank=True)
    attendance_window = models.IntegerField(default=15, help_text="Attendance window in minutes")
    
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    
    
    def activate(self):
        if self.status == 'scheduled':
            self.status = 'active'
            self.actual_start = timezone.now()
            self.save()
            return True
        return False
    
    def end_class(self):
        if self.status == 'active':
            self.status = 'completed'
            self.actual_end = timezone.now()
            self.save()
            return True
        return False
    
    def cancel_class(self):
        if self.status in ['scheduled', 'active']:
            self.status = 'cancelled'
            self.save()
            return True
        return False
    
    def is_active(self):
        return self.status == 'active'
    
    # New methods for attendance control
    def activate_attendance(self):
        """Facilitator activates the attendance marking button"""
        if self.is_active():
            self.attendance_active = True
            self.attendance_activated_at = timezone.now()
            self.save()
            return True
        return False
        
    def deactivate_attendance(self):
        """Facilitator deactivates the attendance marking button"""
        if self.attendance_active:
            self.attendance_active = False
            self.save()
            return True
        return False
    
    def is_attendance_window_open(self):
        """Check if the attendance window is still open"""
        if not self.attendance_active or not self.attendance_activated_at:
            return False
            
        window_end = self.attendance_activated_at + timezone.timedelta(minutes=self.attendance_window)
        return timezone.now() <= window_end






# Model for attendance tracking
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    )
    
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    join_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True)
    self_marked = models.BooleanField(default=False)
    marked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['live_class', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.live_class.title} - {self.status}"
    
    def mark_present(self):
        if not self.join_time:
            self.join_time = timezone.now()
            
        if self.live_class.actual_start and self.join_time > self.live_class.actual_start + timezone.timedelta(minutes=15):
            self.status = 'late'
        else:
            self.status = 'present'
        self.save()
    
    def mark_leave(self):
        if self.join_time and not self.leave_time:
            self.leave_time = timezone.now()
            self.duration = self.leave_time - self.join_time
            self.save()
            
    # Method for student self-marking with button
    def self_mark_attendance(self):
        """Students mark their own attendance by clicking a button"""
        if self.live_class.is_active() and self.live_class.attendance_active:
            self.status = 'present'
            self.self_marked = True
            self.marked_at = timezone.now()
            
            # Still track join time for duration calculations
            if not self.join_time:
                self.join_time = timezone.now()
                
            # Check if late based on when class started
            if self.live_class.actual_start and self.join_time > self.live_class.actual_start + timezone.timedelta(minutes=15):
                self.status = 'late'
                
            self.save()
            return True
        return False
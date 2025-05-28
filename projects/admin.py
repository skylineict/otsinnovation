from django.contrib import admin
from .models import Project, ProjectSubmission, ProjectAttendance


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'project_type', 'status', 'deadline', 'created_at')
    list_filter = ('project_type', 'status', 'course', 'deadline')
    search_fields = ('title', 'course__name')
    filter_horizontal = ('cohorts',)
    date_hierarchy = 'deadline'
    ordering = ('-created_at',)


@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'submitted_by', 'cohort', 'submitted_at', 'score', 'is_approved')
    list_filter = ('is_approved', 'submitted_at', 'project__course')
    search_fields = ('project__title', 'submitted_by__username', 'cohort__name')
    autocomplete_fields = ('project', 'submitted_by', 'cohort')
    readonly_fields = ('submitted_at',)


@admin.register(ProjectAttendance)
class ProjectAttendanceAdmin(admin.ModelAdmin):
    list_display = ('submission', 'student', 'timestamp')
    search_fields = ('submission__project__title', 'student__username')
    autocomplete_fields = ('submission', 'student')
    readonly_fields = ('timestamp',)

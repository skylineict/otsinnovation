from django.contrib import admin
from .models import CourseMonthlyRequirement, ComplianceRecord, StudentPoint


@admin.register(CourseMonthlyRequirement)
class CourseMonthlyRequirementAdmin(admin.ModelAdmin):
    list_display = ('course', 'month', 'score_requirement', 'created_at')
    list_filter = ('course', 'month')
    search_fields = ('course__name',)
    ordering = ('-month',)


@admin.register(ComplianceRecord)
class ComplianceRecordAdmin(admin.ModelAdmin):
    list_display = ('registration', 'month', 'total_score', 'is_compliant', 'warning_sent', 'created_at')
    list_filter = ('is_compliant', 'warning_sent', 'month')
    search_fields = ('registration__user__username', 'registration__course__name')
    ordering = ('-month',)
    readonly_fields = ('total_score', 'is_compliant', 'warning_sent', 'created_at')


@admin.register(StudentPoint)
class StudentPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'total_points', 'updated_at')
    list_filter = ('course',)
    search_fields = ('user__username', 'course__name')
    ordering = ('-updated_at',)


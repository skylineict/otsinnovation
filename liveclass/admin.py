from django.contrib import admin
from .models import LiveClass, LiveClassAttendance

@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'course', 'facilitator', 'start_time', 'end_time', 'status', 'enable_attendance', 'created_at')
    list_filter = ('status', 'enable_attendance', 'course')
    search_fields = ('topic', 'course__name', 'facilitator__username')
    readonly_fields = ('created_at',)
    ordering = ('-start_time',)

@admin.register(LiveClassAttendance)
class LiveClassAttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'live_class', 'student', 'timestamp', 'points_awarded')
    list_filter = ('live_class',)
    search_fields = ('student__username', 'student__email', 'live_class__topic')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

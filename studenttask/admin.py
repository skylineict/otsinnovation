from django.contrib import admin
from .models import Task, Task_collections


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'links')
    search_fields = ('task',)
    readonly_fields = ('id',)
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('task', 'task_img', 'links', 'task_description')
        }),
    )


@admin.register(Task_collections)
class TaskCollectionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'status', 'links')
    list_filter = ('status',)
    search_fields = ('task', 'student__username', 'student__phone', 'student__email')
    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('student', 'task', 'status', 'screen_short', 'links')
        }),
    )

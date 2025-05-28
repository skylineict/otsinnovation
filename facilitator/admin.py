from django.contrib import admin
from .models import FacilitatorRegistration

@admin.register(FacilitatorRegistration)
class FacilitatorRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'approved', 'registration_date', 'rejection_reason', 'rejection_timestamp')
    list_filter = ('approved', 'registration_date', 'rejection_timestamp')
    search_fields = ('user__username', 'user__email', 'course__name', 'rejection_reason')
    readonly_fields = ('registration_date', 'rejection_timestamp')
    ordering = ('-registration_date',)

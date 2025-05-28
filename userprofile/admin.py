from django.contrib import admin
from .models import Profiles


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone_num', 'state', 
        'city', 'status', 'occupation', 'created'
    )
    search_fields = (
        'first_name', 'last_name', 'phone_num', 
        'state', 'city', 'local_govt', 'user__username', 'user__phone'
    )
    list_filter = ('status', 'state', 'occupation', 'laptop', 'certifcate')
    readonly_fields = ('id', 'created')
    fieldsets = (
        ('Personal Info', {
            'fields': (
                'first_name', 'last_name', 'phone_num', 
                'contact_add', 'state', 'city', 'local_govt'
            )
        }),
        ('User Link & Picture', {
            'fields': ('user', 'uplaod_picture')
        }),
        ('Application Details', {
            'fields': (
                'occupation', 'laptop', 'certifcate', 
                'sponsorship', 'status'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created')
        }),
    )

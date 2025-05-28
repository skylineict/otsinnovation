from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'email', 'is_admin', 'is_staff', 'is_facilitator', 'is_verified_facilitator', 'date_joined')
    list_filter = ('is_admin', 'is_staff', 'is_facilitator', 'is_verified_facilitator', 'is_active')
    search_fields = ('phone', 'username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('username', 'email', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_admin', 'is_facilitator', 'is_verified_facilitator')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')


admin.site.register(MyUser, MyUserAdmin)

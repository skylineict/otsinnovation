from django.contrib import admin
from .models import Cohort, CohortLeaderNomination, Recapcourse, Recapsesion

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'leader', 'whatsapp_link', 'created_at')
    search_fields = ('name', 'course__name', 'leader__username')
    list_filter = ('course', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ('students',)  # For ManyToMany field with better UI


@admin.register(CohortLeaderNomination)
class CohortLeaderNominationAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'nominator', 'nominee', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('cohort__name', 'nominator__username', 'nominee__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Recapcourse)
class RecapcourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Recapsesion)
class RecapsesionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'link', 'courses', 'image')
    search_fields = ('title', 'courses__name')
    list_filter = ('date', 'courses')
    ordering = ('-date',)

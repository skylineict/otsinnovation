from django.contrib import admin
from .models import PaymentDetail, CourseRegistration, Transaction, Course

@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'full_name', 'created_at', 'is_approved')
    search_fields = ('user__username', 'user__email', 'full_name', 'course__name')
    list_filter = ('course', 'is_approved', 'created_at')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)



@admin.register(Course)
class Course(admin.ModelAdmin):
        list_display = ('id', 'description', 'name', 'amount', 'duration', 'facilitators')


@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'registration', 
        'payment_option', 
        'payment_completed', 
        'amount_paid', 
        'remaining_amount', 
        'virtual_account_number', 
        'virtual_account_bank', 
        'virtual_account_name',
        'timestamp',
        'manually_verified',
        'manual_reference',
        

    )
    search_fields = (
        'registration__user__username', 
        'registration__user__email', 
        'virtual_account_number',
        'virtual_account_name'
    )
    list_filter = ('payment_option','payment_completed', 'timestamp')
    readonly_fields = ('id', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'transaction_reference', 
        'amount', 'status', 'method', 'transaction_date'
    )
    search_fields = ('transaction_reference', 'payment_detail__registration__user__username')
    list_filter = ('status', 'method', 'transaction_date')
    readonly_fields = ('id', 'transaction_date')
    ordering = ('-transaction_date',)

from django.contrib import admin
from .models import Course, CourseRegistration, Transaction, PaymentDetail




@admin.register(CourseRegistration)
class CourseReg(admin.ModelAdmin):
    list_display = ('id', 'full_name','course','training_mode','internship','created_at','user', 'is_approved')    

@admin.register(PaymentDetail)
class CoursePayment(admin.ModelAdmin):
    list_display = ('id','registration','payment_option','amount_paid','first_payment_date', 'second_payment_date','payment_completed', "flutterwave_ref",'virtual_account_number','virtual_account_bank','virtual_account_name','timestamp', 'reminder_sent', 'payment_status', 'payment_option')
    list_filter = ('payment_option', 'timestamp')
    search_fields = ('registration__full_name', 'payment_option', 'amount_paid', 'payment_status')
    ordering = ('timestamp',)

@admin.register(Transaction)
class RegTransation(admin.ModelAdmin):
    list_display = ('id','payment','transaction_reference','method','status','transaction_date','notes','amount')
    list_filter = ('transaction_date', 'status')
    search_fields = ('transaction_reference', 'method', 'status')
    ordering = ('transaction_date',)


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ('id','name','description','amount','duration','facilitators', 'created_at','updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'facilitators')
    ordering = ('created_at',)
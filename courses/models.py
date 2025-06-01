
from django.db import IntegrityError, models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from decimal import Decimal
from django.core.exceptions import ValidationError
import pyotp
import base64
import os
from venv import logger
from registration.models import MyUser
from django.conf import settings
from django.core.mail import send_mail

PAYMENT_METHOD_CHOICES = [
    ('bank_transfer', 'Bank Transfer'),
    ('flutterwave', 'Flutterwave'),
    ('manual', 'Manual Approval'),  # NEW: Added 'manual' method to support manual approval without payment
]
PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('failed', 'Failed'),
]
TRAINING_MODE_CHOICES = (
    ('online', 'Online'),
    ('physical', 'Physical'),
)

class Course(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)
    facilitators = models.OneToOneField(
        MyUser, blank=True, null=True, related_name='facilitated_course', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CourseRegistration(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    full_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    training_mode = models.CharField(max_length=200, choices=TRAINING_MODE_CHOICES)
    internship = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    admission_passcode = models.CharField(max_length=8, null=True, blank=True, unique=True)
    account_suspended = models.BooleanField(default=False)
    reward_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.full_name} - {self.course.name}"

    def generate_admission_passcode(self):
        if not self.admission_passcode and self.is_approved:
            max_attempts = 10
            for _ in range(max_attempts):
                secret = base64.b32encode(os.urandom(10)).decode('utf-8')
                totp = pyotp.TOTP(secret, digits=6)
                code = totp.now()[:4]
                passcode = f"OTS-{code}"
                if not CourseRegistration.objects.filter(admission_passcode=passcode).exists():
                    self.admission_passcode = passcode
                    self.save(update_fields=["admission_passcode"])
                    break
            else:
                raise ValueError("Unable to generate a unique passcode after multiple attempts")
        return self.admission_passcode

   
    def manual_approve(self, admin_user):
        """
        Manually approve the registration without requiring payment.
        Args:
            admin_user (MyUser): The admin performing the approval
        """
        # NEW: Validate that the registration is not already approved
        if self.is_approved:
            logger.warning(f"Registration {self.id} already approved.")
            raise ValidationError("This registration is already approved.")

      
        if self.account_suspended:
            raise ValidationError("Cannot approve a suspended account.")

        self.is_approved = True
        self.generate_admission_passcode()
        self.save(update_fields=["is_approved", "admission_passcode"])

           
        payment_detail, created = PaymentDetail.objects.get_or_create(
                registration=self,
                defaults={
                    'amount_paid': Decimal('0.00'),
                    'payment_option': 'none',  # NEW: Use 'none' to indicate no payment required
                    'manually_verified': True,
                    'manual_reference': f"MANUAL-APPROVAL-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    'payment_completed': True,  # NEW: Mark as completed since no payment is needed
                }
            )
        if not created:
                # NEW: Update existing PaymentDetail for manual approval
                payment_detail.manually_verified = True
                payment_detail.manual_reference = f"MANUAL-APPROVAL-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                payment_detail.payment_completed = True
                payment_detail.save()

            # NEW: Create a transaction record for auditing manual approval
        Transaction.objects.create(
                payment=payment_detail,
                transaction_reference=f"MANUAL-APPROVAL-{self.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                amount=Decimal('0.00'),
                method='manual',  # NEW: Use 'manual' method from PAYMENT_METHOD_CHOICES
                status='approved',
                notes=f"Manual approval by {admin_user.email} without payment"
            )

            # NEW (EMAIL): Send email notification to the user upon manual approval
            # NEW (EMAIL): Checks if user exists and has a valid email address to avoid errors
        if self.user and self.user.email:
                send_mail(
                        subject=f"Admission Confirmation for {self.course.name}",
                        message=(
                            f"Dear {self.full_name},\n\n"
                            f"Congratulations! Your registration for {self.course.name} has been approved.\n"
                            f"Your admission passcode is: {self.admission_passcode}\n\n"
                            f"Please use this passcode to access your course materials. "
                            f"If you have any questions, contact our support team.\n\n"
                            f"Best regards,\nCourse Administration Team"),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[self.user.email],
                        fail_silently=True,)
                   
                
          

           
        if self.course.facilitators and self.course.facilitators.email:
                send_mail(
                        subject=f"New Student Approved for {self.course.name}",
                        message=(
                            f"Dear {self.course.facilitators.full_name},\n\n"
                            f"Student {self.full_name} has been manually approved for your course {self.course.name} "
                            f"by {admin_user.email}.\n"
                            f"Admission passcode: {self.admission_passcode}\n\n"
                            f"Please ensure the student is onboarded appropriately.\n\n"
                            f"Best regards,\nCourse Administration Team"),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[self.course.facilitators.email],
                        fail_silently=True,)
                    # NEW (EMAIL): Log successful facilitator email sending
                   

class PaymentDetail(models.Model):
    PAYMENT_OPTION_CHOICES = [
        ('installment', 'Installment (50%)'),
        ('full', 'Full Payment (100%)'),
        ('none', 'No Payment Required'),  # NEW: Added 'none' option for manual approvals without payment
    ]
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    registration = models.OneToOneField('CourseRegistration', on_delete=models.CASCADE, related_name='payment_detail')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    first_payment_date = models.DateTimeField(null=True, blank=True)
    second_payment_date = models.DateTimeField(null=True, blank=True)
    payment_completed = models.BooleanField(default=False)
    flutterwave_ref = models.CharField(max_length=100, null=True, blank=True, unique=True)
    virtual_account_number = models.CharField(max_length=20, null=True, blank=True)
    virtual_account_bank = models.CharField(max_length=50, null=True, blank=True)
    virtual_account_name = models.CharField(max_length=100, null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTION_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    manually_verified = models.BooleanField(default=False)
    manual_reference = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def update_payment(self, payment_amount, transaction_reference=None, method=None, status='pending', notes=None):
        """
        Update PaymentDetail and associated Transaction, ensuring idempotency.
        """
        if self.payment_completed:
            logger.warning(f"Payment already completed for tx_ref: {transaction_reference}")
            return

        if self.payment_option == 'installment':
            expected_amount = self.registration.course.amount * Decimal('0.5')
            if payment_amount != expected_amount and status == 'approved':
                raise ValidationError(f"Installment payment must be {expected_amount}.")
        elif self.payment_option == 'full':
            expected_amount = self.registration.course.amount
            if payment_amount != expected_amount and status == 'approved':
                raise ValidationError(f"Full payment must be {expected_amount}.")

        try:
            # Update or create Transaction
            transaction, created = Transaction.objects.update_or_create(
                payment=self,
                transaction_reference=transaction_reference or f"TXN-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                defaults={
                    'amount': payment_amount,
                    'method': method or 'unknown',
                    'status': status,
                    'notes': notes or f"Payment for {self.payment_option} option",
                    'bank_name': self.virtual_account_bank if method == 'bank_transfer' else None
                }
            )
            if created:
                logger.info(f"Created new Transaction for tx_ref: {transaction_reference}")
            else:
                logger.info(f"Updated existing Transaction for tx_ref: {transaction_reference}")

            # Update PaymentDetail if status is approved
            if status == 'approved':
                self.amount_paid += payment_amount
                if not self.first_payment_date:
                    self.first_payment_date = timezone.now()
                else:
                    self.second_payment_date = timezone.now()

                partial_payment_threshold = self.registration.course.amount * Decimal(0.5)
                if self.amount_paid >= partial_payment_threshold and not self.registration.is_approved:
                    self.registration.is_approved = True
                    self.registration.generate_admission_passcode()
                if self.amount_paid >= self.registration.course.amount:
                    self.payment_completed = True

                if transaction_reference:
                    self.flutterwave_ref = transaction_reference

                self.save()
                self.registration.save()

        except IntegrityError as e:
            logger.error(f"IntegrityError updating payment for tx_ref: {transaction_reference}: {e}")
            if 'UNIQUE constraint failed' in str(e):
                logger.warning(f"Transaction already exists for tx_ref: {transaction_reference}")
            else:
                raise

    def set_payment_option(self, option):
        if option not in [choice[0] for choice in self.PAYMENT_OPTION_CHOICES]:
            raise ValidationError(f"Invalid payment option: {option}")
        if self.amount_paid > 0:
            raise ValidationError("Cannot change payment option after payments have been made")
        self.payment_option = option
        self.save(update_fields=['payment_option'])

    @property
    def payment_status(self):
        if self.payment_completed:
            return "Completed"
        elif self.amount_paid > 0:
            if self.is_payment_overdue:
                self.registration.is_approved = False
                self.registration.account_suspended = True
                self.registration.save(update_fields=["is_approved", "account_suspended"])
                return "Overdue"
            return "Partially Paid"
        # NEW: Return 'Manually Approved' for manual approvals without payment
        elif self.manually_verified:
            return "Manually Approved"
        return "Pending"

    @property
    def remaining_amount(self):
        # NEW: Return zero for manual approvals with 'none' payment option
        if self.payment_option == 'none':
            return Decimal('0.00')
        return max(0, self.registration.course.amount - self.amount_paid)

    @property
    def is_payment_overdue(self):
        # NEW: Skip overdue checks for manual approvals
        if self.payment_option == 'none':
            return False
        if self.first_payment_date and not self.payment_completed:
            deadline = self.first_payment_date + timezone.timedelta(days=30)
            return timezone.now() > deadline
        return False

class Transaction(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    payment = models.ForeignKey(PaymentDetail, on_delete=models.CASCADE, related_name='transactions')
    transaction_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction {self.transaction_reference} for {self.payment.registration.full_name}"

class SuspensionFine(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, editable=False, alphabet='abcdefghijklmnqszxcvopl1234567890')
    registration = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE, related_name='suspension_fines')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    flutterwave_ref = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_paid(self, transaction_reference, payment_method='unknown'):
        self.paid = True
        self.payment_date = timezone.now()
        self.flutterwave_ref = transaction_reference
        self.save()
        Transaction.objects.create(
            payment=self.registration.payment_detail,
            transaction_reference=transaction_reference,
            amount=self.amount,
            method=payment_method,
            status='approved',
            notes=f"Suspension fine payment"
        )
        # send_mail(
        #     subject="Suspension Fine Paid",
        #     message=f"Your suspension fine of {self.amount} for {self.registration.course.name} has been paid. Please contact an admin to unlock your account.",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[self.registration.user.email],
        #     fail_silently=True,
        # )

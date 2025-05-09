from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import PaymentDetail, CourseRegistration
class Command(BaseCommand):
    help = 'Send payment reminders to users with pending payments 7 days before suspension'

    def handle(self, *args, **options):
        today = timezone.now().date()
        reminder_date = today + timedelta(days=7)  # 7 days from now

        # Find PaymentDetails where:
        # - payment is partial (amount_paid > 0 and not payment_completed)
        # - first_payment_date + 30 days == today + 7 days
        # - reminder not yet sent
        pending_payments = PaymentDetail.objects.filter(
            amount_paid__gt=0,
            payment_completed=False,
            reminder_sent=False,
            first_payment_date__date=(reminder_date - timedelta(days=30)).date()
        )

        for payment in pending_payments:
            user = payment.registration.user
            if user and user.email:
                remaining_amount = payment.remaining_amount
                deadline = payment.first_payment_date + timedelta(days=30)
                send_mail(
                    subject="Payment Reminder: Complete Your Course Payment",
                    message=(
                        f"Dear {user.full_name},\n\n"
                        f"You have a pending payment for the course '{payment.registration.course.name}'.\n"
                        f"Amount remaining: {remaining_amount}\n"
                        f"Please complete your payment by {deadline.strftime('%Y-%m-%d')} to avoid account suspension.\n\n"
                        f"Best regards,\nE-Learning Team"
                    ),
                    from_email="noreply@elearning.com",
                    recipient_list=[user.email],
                )
                payment.reminder_sent = True
                payment.save(update_fields=["reminder_sent"])
                self.stdout.write(self.style.SUCCESS(f"Sent reminder to {user.email}"))
            else:
                self.stdout.write(self.style.WARNING(f"No email for user {user.id}"))
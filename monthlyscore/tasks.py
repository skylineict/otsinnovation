from celery import shared_task
from monthlyscore.models import CourseMonthlyRequirement
from django.utils import timezone

@shared_task
def reset_monthly_scores():
    """Reset score_requirement to 0 for requirements older than one month."""
    # current_date = timezone.now().date()
    current_date = timezone.now()
    requirements = CourseMonthlyRequirement.objects.filter(score_requirement__gt=0)
    reset_count = 0

    for requirement in requirements:
        if requirement.reset_if_expired(current_date):
            reset_count += 1

    return f"Successfully reset {reset_count} monthly score requirements."
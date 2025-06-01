from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')
app.conf.enable_utc = False
app.conf.update(timezone='Africa/Lagos')
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    # 'send-mail-every-2-minutes': {
    #     'task': 'reg.tasks.send_email_to_users',
    #     'schedule': crontab(minute='*/2'),
    # },
    'reset-monthly-scores': {
        'task': 'monthlyscore.tasks.reset_monthly_scores',
        'schedule': crontab(minute='*/5'),
    },
    # 'reset-monthly-scores': {
    #     'task': 'monthlyscore.tasks.reset_monthly_scores',
    #     'schedule': crontab(minute=1, hour=0, day_of_month=1),
    # },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
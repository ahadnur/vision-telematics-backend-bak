from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('vision-telematics-backend')


app.config_from_object('django.conf:settings', namespace='CELERY')


# beat setting
# app.conf.beat_schedule = {
#     'send_order_mail' : {
#         'task' : 'apps.orders.tasks.send_order_mail',
#     }
# }

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from celery import task
from celery import shared_task
from .utils import regular_refresh
# We can have either registered task
@task(name='autorefresh')
def send_import_summary():
    print('starting periodic task')
    regular_refresh()
# or

@shared_task
def send_notifiction():
     print('Here I am')
     # Another trick
from celery import task
from celery import shared_task
from .utils import regular_refresh
# We can have either registered task
@shared_task(name='autorefresh')
def start_autorefresh():
    print('starting periodic task')
    regular_refresh()
# or

@shared_task
def send_notifiction():
     print('Here I am')
     # Another trick
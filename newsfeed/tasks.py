from celery import Celery
from .utils import regular_refresh
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsriver.settings')
app = Celery('newsfeed', broker='pyamqp://guest@localhost//')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

@app.task(name='autorefresh_task', bind=True)
def auto_refresh():
    regular_refresh()

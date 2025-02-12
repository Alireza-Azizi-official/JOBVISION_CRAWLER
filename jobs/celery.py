from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Setting default Django settings for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Creating a Celery instance named 'jobs'
app = Celery('jobs')

# Configuring Celery to use Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Ensuring Celery retries broker connection on startup
app.conf.broker_connection_retry_on_startup = True

# Setting up a schedule for tasks with Celery Beat
app.conf.beat_schedule = {
    'scrape-jobs-every-midnight': {
        'task': 'jobs.tasks.scrape_jobs',  # The task to be executed
        'schedule': crontab(minute=0, hour=0),  # Schedule: every day at 00:00
    },
}

if __name__ == '__main__':
    app.start()

from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery import Celery
import os

# Setting default Django settings for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Creating a Celery instance named 'jobs'
app = Celery('jobs')

# Configuring Celery to use Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

# Setting up a schedule for tasks with Celery Beat
app.conf.beat_schedule = {
    # Task schedule to run every midnight
    'scrape-jobs-every-midnight': {
        'task': 'jobs.tasks.scrape_jobs',  # The task to be executed
        'schedule': crontab(minute=0, hour=0),  # Schedule: every day at 00:00
    },
}

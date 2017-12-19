#!/usr/bin/env python
"""
Holds generic celery configuration for Laten, and
similar services that you may want to implement on top
of this
"""


from celery.schedules import crontab
from datetime import timedelta
from laten.configregistry import Configuration

result_backend = "mongodb"


mongodb_backend_settings = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "celery_results", 
    "taskmeta_collection": "task_results",
}


config = Configuration()

beat_schedule = {
    'check_urls' : {
	'task' : 'laten.tasks.check_urls',
	'schedule' : timedelta(minutes=config.sample_interval),
    'relative': True,
	'args' : (),
    },   
}

# celery settings I figured through my work
# with it in high load production environment
worker_max_tasks_per_child = 24
worker_max_memory_per_child = 800000
task_time_limit = config.task_timeout
worker_concurrency = 4
task_eager_propagates = True

del config



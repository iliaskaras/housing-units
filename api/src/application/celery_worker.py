from celery import Celery

from application.infrastructure.configurations.models import Configuration

Configuration.initialize()

celery = Celery(__name__)
celery.conf.broker_url = Configuration.get().celery_broker_url
celery.conf.result_backend = Configuration.get().celery_result_backend

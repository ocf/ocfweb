"""Load Celery tasks for account submission.

This module is responsible for instantiating the Celery tasks used for account
creation using our special credentials. Other modules should import from here,
rather than from ocflib directly.
"""
import ssl

from celery import Celery
from django.conf import settings
from ocflib.account.submission import get_tasks as real_get_tasks

celery_app = Celery(
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)
# TODO: use ssl verification
celery_app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE,
}
# `redis_backend_use_ssl` is an OCF patch which was proposed upstream:
# https://github.com/celery/celery/pull/3831
celery_app.conf.redis_backend_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE,
}

# TODO: stop using pickle
celery_app.conf.task_serializer = 'pickle'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = {'pickle'}

_tasks = real_get_tasks(celery_app)

create_account = _tasks.create_account
validate_then_create_account = _tasks.validate_then_create_account
get_pending_requests = _tasks.get_pending_requests
approve_request = _tasks.approve_request
reject_request = _tasks.reject_request
change_password = _tasks.change_password

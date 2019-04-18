import logging

from celery.utils.log import logger as celery_logger

from .celery import app
from .email import send_email

logger = logging.getLogger(__name__)


@app.task
def send_async_email_debug(subject, message, recipient):
    logger.info(subject, message, recipient)
    celery_logger.info(subject, message, recipient)


@app.task
def send_async_email(subject, message, recipient):
    send_email(subject, message, recipient)
from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from .email import send_new_email_registration

logger=get_task_logger(__name__)

@task(name="send_new_registration_email_task")
def send_new_registration_email_task(name,ci,email):
    print("Sent new registration email")
    logger.info("Sent new registration email")
    return send_new_email_registration(name,ci,email)
@shared_task
def add(x, y):
    return x + y
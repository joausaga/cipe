from celery.decorators import task
from celery.utils.log import get_task_logger
from .email import send_new_email_registration,send_approved_email

logger=get_task_logger(__name__)

@task(name="send_new_registration_email_task")
def send_new_registration_email_task(name,position,institution):
    logger.info("Sending email to moderators ... ")
    return send_new_email_registration(name,position,institution)


@task(name="send_approved_email_task")
def send_approved_email_task(name,slug,email):
    logger.info("Sent approve email task")
    return send_approved_email(name,slug,email)

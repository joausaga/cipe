from celery.decorators import task
from celery.utils.log import get_task_logger
from .email import send_new_email_registration,send_approved_email,daily_verification_of_registrants_whose_period_abroad_has_ended
from app.models import Scientist,NotificationUpdateScientist
from datetime import date 
import datetime
from celery import shared_task
logger=get_task_logger(__name__)

@task(name="send_new_registration_email_task")
def send_new_registration_email_task(name,position,institution):
    logger.info("Sending email to moderators ... ")
    return send_new_email_registration(name,position,institution)


@task(name="send_approved_email_task")
def send_approved_email_task(name,slug,email):
    logger.info("Sent approve email task")
    return send_approved_email(name,slug,email)


@shared_task
def daily_verification_of_registrants_whose_period_abroad_has_ended_task():
    logger.info("Daily verification")
    daily_verification_of_registrants_whose_period_abroad_has_ended()

@shared_task
def disabled_scientist_end_period_past_a_month():
    scientists=Scientist.objects.filter(approved=True).filter(end_abroad_period__lte=date.today()-datetime.timedelta(days=30))
    for scientist in scientists:
        notification=NotificationUpdateScientist.objects.get_or_create(scientist=scientist)[0]
        if notification.it_has_been_notified:
            scientist.approved=False
            scientist.save()

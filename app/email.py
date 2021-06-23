
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage 
from django.conf import settings
from .models import Scientist,NotificationScientist
from datetime import date
def send_new_email_registration(name,position, institution):

    context = {
        'name': name,
        'position':position,
        'institution':institution
    }
    email_subject = 'Nuevo Registro ingresado'
    html_message = render_to_string('email/new_email_registration.html', context)
    email = EmailMessage(
        subject=email_subject,
        body=html_message,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to=[settings.MODERATOR_EMAIL_ADDRESSES],
        )
    email.content_subtype = 'html' 
    return email.send()

def send_approved_email(name,slug,to_email):

    context = {
        'name': name,
        'slug': slug,
    }
    email_subject = 'Tu registro en el sitio Investigadores Paraguayos en el Mundo ha sido aprobado'
    html_message = render_to_string('email/approved_email.html', context)
    email = EmailMessage(
        subject=email_subject,
        body=html_message,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
        )
    email.content_subtype = 'html' 
    return email.send()
    
def daily_verification_of_registrants_whose_period_abroad_has_ended():
    scientists=Scientist.objects.filter(approved=True).filter(end_abroad_period__lte=date.today())
    for scientist in scientists:
        """
        Look for a valid notification type ABROAD_PERIOD_EXPIRATION of the users. If the result is a notification objects, it means the user
        had been previously notified, else it means it had not been notified
        """
        notification=NotificationScientist.objects.filter(scientist=scientist).filter(created_at__gte=scientist.end_abroad_period).filter(type="ABROAD_PERIOD_EXPIRATION").first()
        if notification:
            continue
        if(send_email_update_abroad_end_return(scientist)):
            NotificationScientist.objects.create(scientist=scientist,type="ABROAD_PERIOD_EXPIRATION")

def send_email_to_all_active_scientitst():
    scientists=Scientist.objects.filter(approved=True)
    for scientist in scientists:
        send_email_update_abroad_end_return(scientist)


def send_email_update_abroad_end_return(scientist):
        email_subject = "Tu estancia en el extranjero ha finalizado, si no es así, favor, actualiza tus datos"
        context = {
        'name': scientist.first_name +" "+ scientist.last_name,
        'slug': scientist.slug,
        }
        html_message = render_to_string('email/end_date_of_return.html', context)
        email = EmailMessage(
            subject=email_subject,
            body=html_message,
            from_email= settings.DEFAULT_FROM_EMAIL,
            to=[scientist.email],
            )
        email.content_subtype = 'html' 
        return email.send()

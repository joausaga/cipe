
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage ,send_mass_mail
from django.conf import settings
from .models import Scientist
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
    scientists=Scientist.objects.filter(approved=True).filter(end_abroad_period=date.today())
    email_subject = "Tu estancia en el extranjero ha finalizado, si no es así, favor, actualiza tus datos"
    for scientist in scientists:
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
        email.send()

def send_mail_to_update_expected_date_of_return():
    scientists=Scientist.objects.filter(approved=True)
    email_subject = 'Actualizar fecha de retorno'
    for scientist in scientists:
        context = {
            'name': scientist.first_name +" "+ scientist.last_name,
            'slug': scientist.slug,
        }
        html_message = render_to_string('email/update_expected_return_date.html', context)
        email = EmailMessage(
            subject=email_subject,
            body=html_message,
            from_email= settings.DEFAULT_FROM_EMAIL,
            to=[scientist.email],
            )
        email.content_subtype = 'html' 
        email.send()

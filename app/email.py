
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

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

def send_approved_email(name,slug,email):

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
        to=[email],
        )
    email.content_subtype = 'html' 
    return email.send()
    

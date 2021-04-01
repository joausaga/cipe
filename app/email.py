
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import send_mail

def send_new_email_registration(name,position, institution):

    context = {
        'name': name,
        'position':position,
        'institution':institution
    }
    email_subject = 'Nuevo Registro ingresado(cipe)'
    html_message = render_to_string('email/new_email_registration.html', context)
    plain_message = strip_tags(html_message)
    return send_mail(
        email_subject, plain_message,
        settings.ADMIN_EMAIL_ADDRESS,settings.EMAILS_FROM_MODERATOR,html_message=html_message, fail_silently=True
    )

def send_approved_email(name,slug,email):

    context = {
        'name': name,
        'slug': slug,
    }

    email_subject = 'Tu registro ha sido aprovado'
    html_message = render_to_string('email/approved_email.html', context)
    plain_message = strip_tags(html_message)

    return send_mail(
        email_subject, plain_message,
        settings.ADMIN_EMAIL_ADDRESS,[email,],
        html_message=html_message, fail_silently=True
    )
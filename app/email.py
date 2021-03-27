
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_new_email_registration(name, ci, email):

    context = {
        'name': name,
        'email': email,
        'ci': ci,
    }

    email_subject = 'New registration (cipe)'
    email_body = render_to_string('email/new_email_registration.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL,settings.EMAILS_FROM_MODERATOR,
    )
    return email.send(fail_silently=False)

def send_approved_email(name, ci, email):

    context = {
        'name': name,
        'email': email,
        'ci': ci,
    }

    email_subject = 'You have been Approved'
    email_body = render_to_string('email/approved_email.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL,[email,],
    )
    return email.send(fail_silently=False)
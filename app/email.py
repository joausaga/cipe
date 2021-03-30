
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
    email_subject = 'New registration (cipe)'
    html_message = render_to_string('email/new_email_registration.html', context)
    plain_message = strip_tags(html_message)
    return send_mail(
        email_subject, plain_message,
        settings.DEFAULT_FROM_EMAIL,settings.EMAILS_FROM_MODERATOR,html_message=html_message, fail_silently=True
    )

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
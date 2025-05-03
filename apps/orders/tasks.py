from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def send_order_email(subject, template_name, context, recipient_email):
    html_content = render_to_string(template_name, context)
    print("EMail host user: ", settings.EMAIL_HOST_USER)
    print("Email host pass: ", settings.EMAIL_HOST_PASSWORD)
    msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [recipient_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    
    return "Done"
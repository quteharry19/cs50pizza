from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf.global_settings import EMAIL_HOST_USER

def send_HTML_Email(to='', subject='', template_name='', context=''):
    msg_html = render_to_string(template_name,context=context)
    msg = EmailMessage(subject=subject,body=msg_html,from_email="Pinnochio's Pizza & Subs",to=to)
    msg.content_subtype = "html"
    print('mail send successfully')
    return msg.send()

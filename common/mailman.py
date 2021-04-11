import os

from django.core import mail
from django.template.loader import render_to_string
from booking.models import Appointment


def sendingmail(instance: Appointment) -> bool:

    context = {
        'appointment': instance,
    }

    html = render_to_string('email/service_receipt.html', context=context)
    txt = render_to_string('email/service_receipt.txt', context=context)

    try:
        mail.send_mail(
            subject='Clean Service Appointment Info',
            message=txt,
            html_message=html,
            from_email=os.environ.get('MAIL_USER'),
            recipient_list=[instance.email,os.environ.get('MAIL_ADMIN')],
            fail_silently=False
        )
        return True
    except Exception as e:
        print(f'[ERROR] error sending mail: {e}')
        return False

import asyncio
import os
import threading

from booking.models import Appointment
from django.core import mail
from django.template.loader import render_to_string
from threading import Thread


class EmailThread(threading.Thread):
    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run (self):

        hours = self.instance.estimated_time // 60
        minutes = self.instance.estimated_time % 60

        time_text = f'{hours} {"hour" if hours == 1 else "hours" } { " "+str(minutes)+" minutes" if minutes != 0 else ""}'

        context = {
            'appointment': self.instance,
            'estimated_time': time_text
        }

        html = render_to_string('email/service_receipt.html', context=context)
        txt = render_to_string('email/service_receipt.txt', context=context)
        try:
            mail.send_mail(
                subject='Clean Service Appointment Info',
                message=txt,
                html_message=html,
                from_email=os.environ.get('MAIL_USER'),
                recipient_list=[self.instance.email,os.environ.get('MAIL_ADMIN')],
                fail_silently=False
            )
            print(f'[INFO] mail successfully sended to {self.instance.email} service order # {self.instance.id}')
        except Exception as e:
            print(f'[ERROR] error sending mail to {self.instance.email} service order {self.instance.id}: {e}')
             

def send_html_mail(instance: Appointment) -> bool :
    EmailThread(instance).start()
    return True

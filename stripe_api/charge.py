from . import stripe
from booking.models import Appointment
from django.http import request


def create_charge(order_data: request):
    total_cents = int(float(order_data.POST.get('total'))*100)

    try:
        return stripe.Charge.create(
            amount = total_cents,
            currency = 'USD',
            source = order_data.POST.get('stripeToken'),
            receipt_email = order_data.POST.get('email'),
            description = f"product: {order_data.POST.get('area')} email: {order_data.POST.get('email')} cust: {order_data.POST.get('firstname')} {order_data.POST.get('lastname')}"
        )

    except stripe.error.CardError as e:
        print(f'--> in charge: {e}')
        return {
            'err': True,
            'message': e._message,
            'status': e.http_status,
            'code': e.code
        }


# def update_charge(order_data: Appointment, charge_id):
#     return stripe.Charge.update(

#     )
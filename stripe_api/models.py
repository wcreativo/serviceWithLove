# from booking.models import Appointment
# from common.models import CommonData
# from django.db.models import CharField, BooleanField, TextField, IntegerField, ForeignKey, CASCADE, DO_NOTHING


# class StripeCustomer(CommonData):
#     email: str = CharField(verbose_name='customer email', max_length=200)
#     token: str = CharField(verbose_name='stripe token', max_length=200)
#     str_customer_id: str =  CharField(verbose_name='stripe customer id', max_length=200)


# class StripeOrder(CommonData):
#     appointment: Appointment = ForeignKey(Appointment, on_delete=DO_NOTHING)
#     stripe_order_id: str = CharField(verbose_name='stripe order id', max_length=200)
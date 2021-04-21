from . import stripe

def create_card(user, token):
    return stripe.Customer.create_source(user.customer_id, source=token)
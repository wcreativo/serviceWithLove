from . import stripe


def create_charge(order, user, card):
    return stripe.Charge.create(
        amount = int(order.total),
        currency = 'USD',
        description = order.description,
        customer = user.customer_id,
        source = card.card_id,
        metadata = {
            'order_id': order.id
        }
    )
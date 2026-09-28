import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    product = stripe.Product.create(
        name=name,
    )
    return product


def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency="rub",
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url="http://127.0.0.1:8000/payment/success/",
        cancel_url="http://127.0.0.1:8000/payment/cancel/",
    )
    return session

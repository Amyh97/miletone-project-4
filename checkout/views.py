from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
import stripe

from .forms import OrderForm
from bag.contexts import basket_content


def checkout(request):
    basket = request.session.get('basket', {})
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if not basket:
        messages.error(request, 'There is nothing in your basket')
        return redirect(reverse('products'))

    current_basket = basket_content(request)
    basket_total = current_basket['grand_total']
    # stripe required int
    stripe_total = round(basket_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY
    )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'You have forgotten to set a public key')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

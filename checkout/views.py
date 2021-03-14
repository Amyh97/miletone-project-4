from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm


def checkout(request):
    basket = request.session.get('basket', {})
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    if not basket:
        messages.error(request, 'There is nothing in your basket')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': 'test',
    }

    return render(request, template, context)

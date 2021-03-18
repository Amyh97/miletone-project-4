from django.http import HttpResponse
from decimal import Decimal

from .models import Order, OrderItem
from products.models import products
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # data that was input in JS post method
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_address = intent.shipping
        # turn from int to float to 2 places
        grand_total = round(intent.charges.data[0].amount/100, 2)

        # clean data as stripe will store blank strings not None
        for field, value in shipping_address.items():
            if value == '':
                shipping_address.address[field] = None

        # save/update data if save_info was checked
        profile = None
        username = intent.metadata.username

        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user_username=username)
            if save_info:
                profile.default_full_name = shipping_address.name
                profile.default_email = billing_details.email
                profile.default_contact_number = shipping_address.phone
                profile.default_country = shipping_address.address.country
                profile.default_postcode = shipping_address.address.postal_code
                profile.default_town = shipping_address.address.city
                profile.default_street_address1 = shipping_address.address.line1
                profile.default_street_address2 = shipping_address.address.line2
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                        # from JS post method
                        full_name__iexact=shipping_address.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_address.phone,
                        country__iexact=shipping_address.address.country,
                        postcode__iexact=shipping_address.address.postal_code,
                        town_or_city__iexact=shipping_address.address.city,
                        street_address1__iexact=shipping_address.address.line1,
                        street_address2__iexact=shipping_address.address.line2,
                        grand_total=grand_total,
                        original_basket=basket,
                        stripe_pid=pid,
                )
                order_exists = True
                # break while loop as order has been found
                break

            except Order.DoesNotExist:
                # attemps running code 5 times in 5 seconds
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                    content=f'Webhook received: {event["type"]}|\
                        Order is in database', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_address.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_address.phone,
                    country=shipping_address.address.country,
                    postcode=shipping_address.address.postal_code,
                    town_or_city=shipping_address.address.city,
                    street_address1=shipping_address.address.line1,
                    street_address2=shipping_address.address.line2,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                for item_id, specs_in_basket in json.loads(basket).items():
                    for specs, quantity in\
                            specs_in_basket['items_by_specs'].items():
                        specs = specs.split('-')
                        product = products.objects.get(id=item_id)
                        item_id = specs[0]
                        size_len = specs[2]
                        finish_img = specs[3]
                        price = Decimal(specs[4])
                        quantity = int(quantity)
                        orderitem_total = quantity * price
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            size_len=size_len,
                            finish_img=finish_img,
                            price=price,
                            quantity=quantity,
                            orderitem_total=orderitem_total,
                        )
                        order_item.save()
            except Exception as e:
                if order:
                    # delete order if anything goes wrong
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}\
                            | Error: {e}.',
                    status=500)
        return HttpResponse(
                    content=f'Webhook received: {event["type"]}|\
                        Order created in webhook', status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

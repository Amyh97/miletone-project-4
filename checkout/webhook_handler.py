from django.http import HttpResponse
from decimal import Decimal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItem
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def __send_email_confirmation__(self, order):
        """ send emails to customer once order is placed """
        customer_email = order.email
        subject = render_to_string(
            # provide template and context
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            # provide template and context
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            # provide subject, bodt, sender and recipients
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            # list format as there can be multiple recipients
            [customer_email, ]
        )

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
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_full_name = shipping_address.name
                profile.default_email = billing_details.email
                profile.default_contact_number = shipping_address.phone
                profile.default_country = shipping_address.address.country
                profile.default_postcode = shipping_address.address.postal_code
                profile.default_town = shipping_address.address.city
                profile.default_street_address1 = shipping_address.\
                    address.line1
                profile.default_street_address2 = shipping_address.\
                    address.line2
                profile.save()

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
                # break while loop as order has been found
                break

            except Order.DoesNotExist:
                # attemps running code 5 times in 5 seconds
                attempt += 1
                time.sleep(1)

        if Order:
            # order is in system so can send email
            self.__send_email_confirmation__(order)
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
                x = 0
                for item_id in json.loads(basket).items():
                    specs = list(basket.items())[x][1]
                    item_id = list(basket.items())[x]
                    name = specs.split(",")[0].split(":")[1].replace("'", "")
                    # unable to shoren lines, get unexpected indent error
                    image = specs.split(",")[1].split(":", 1)[1].replace("'", "")
                    size_len = specs.split(",")[2].split(":")[1].replace("'", "")
                    finish_img = specs.split(',')[3].split(":")[1].replace("'", "")
                    price = Decimal(specs.split(',')[4].split(":")[1].replace("'", ""))
                    quantity = int(specs.split(',')[5].split(":")[1]
                                   .replace("']", "").replace("'", "").strip())
                    orderitem_total = price * quantity
                    order_item = OrderItem(
                        item_id=item_id,
                        name=name,
                        image=image,
                        order=order,
                        size_len=size_len,
                        finish_img=finish_img,
                        price=price,
                        quantity=quantity,
                        orderitem_total=orderitem_total,
                    )
                    order_item.save()

                    x += 1
            except Exception as e:
                if order:
                    # delete order if anything goes wrong
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]}\
                            | Error: {e}.',
                    status=500)
        # order has been created in webhook, so can now send email
        self.__send_email_confirmation__(order)
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

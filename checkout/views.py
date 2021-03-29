from django.shortcuts import render, redirect, reverse,\
     get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from django.views.decorators.http import require_POST
import stripe
import json

from .forms import OrderForm
from bag.contexts import stripe_basket, basket_content
from .models import OrderItem, Order
from profiles.models import UserProfile
from profiles.forms import ProfileForm


@require_POST
def cache_checkout_data(request):
    """ capture data when save info is checked for logged
    in users """
    try:
        # payment intent id
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],

        }

        # put data user has input to add to order form model
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # commit fale to prevent multiple save events
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
            x = 0
            for item_id in basket.items():
                specs = list(basket.items())[x][1]
                basket = request.session.get('basket', {})
                item_id = list(basket.items())[x][0]
                name = specs.split(",")[0].split(":")[1].replace("'", "")
                image = specs.split(",")[1].split(":", 1)[1].replace("'", "")
                size_len = specs.split(",")[2].split(":")[1].replace("'", "")
                finish_img = specs.split(',')[3].split(":")[1].replace("'", "")
                price = Decimal(specs.split(',')[4].split(":")[1].replace("'", ""))
                quantity = int(specs.split(',')[5].split(":")[1].replace("']", "").replace("'", "").strip())
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

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            messages.error(request, 'There was an error in your form,\
                please double check the information.')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, 'There is nothing in your basket')
            return redirect(reverse('products'))

        current_basket = stripe_basket(request)
        basket_total = current_basket['grand_total']
        # stripe required int
        stripe_total = round(basket_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.default_name,
                    'email': profile.default_email,
                    'phone_number': profile.default_contact_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town,
                    'postcode': profile.default_postcode,
                    'country': profile.default_counrty,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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


def checkout_success(request, order_number):
    """
    handle successful checkouts
    """
    # for use with profiles
    save_info = request.session.get('save_info')
    # the "=order_number" comes from view prams
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # attatch order to profile
        order.user_profile = profile
        order.save()

        # update info if box ticked
        if save_info:
            profile_data = {
                # keys match user profile model
                'default_name': order.full_name,
                'default_email': order.email,
                'default_contact_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town': order.town_or_city,
                'default_postcode': order.postcode,
                # spelling consistant with model
                'default_counrty': order.country,
            }
            user_profile_form = ProfileForm(profile_data,
                                            instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Your order has been processed. \
            Your order number is: {order_number}. A confirmation email is\
            on its way to {order.email}')

    if 'basket' in request.session:
        del request.session['basket']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order
    }

    return render(request, template, context)

from decimal import Decimal
from django.conf import settings
from .views import basket_item


def basket_content(request):
    basket_items = []
    total = 0
    count = 0
    basket = request.session.get('basket', {})
    item = basket_item

    for item in basket.items():
        # item is tuple, element 0 is string version of dict
        split_items = item[0].split(",")
        # get the value after ":" of quantity and price items
        quantity = int(split_items[1].split(":")[1])
        price = split_items[2].split(":")[1]
        # remove excess quote marks from sting
        price_tidy = price.replace("'", "")
        # convert to decimal to do maths on
        float_price = Decimal(price_tidy)
        total += quantity * float_price
        count += quantity
        basket_items.append({
                'item': item
            })

    if total < settings.FREE_DELIVERY:
        # decimal used rather than float as float is more susceptible to errors
        delivery = total * Decimal(settings.DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'count': count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'grand_total': grand_total
    }
    return context

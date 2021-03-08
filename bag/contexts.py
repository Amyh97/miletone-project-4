from decimal import Decimal
from django.conf import settings


def basket_content(request):
    basket_items = []
    total = 0
    count = 0

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

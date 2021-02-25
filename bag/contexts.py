from decimal import Decimal
from django.conf import settings
"""
    basket context processor so that the bag can be
    accessed from any page of the site
"""


def basket_content(request):

    basket_items = []
    total = 0
    # items in basket, services or products
    count = 0

    if total < settings.FREE_DELIVERY:
        """ use decimal rather than float as it is less likely
        to have rounding errors """
        delivery = total * Decimal(settings.DELIVERY_PERCENTAGE)
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
        'free delivery': settings.FREE_DELIVERY,
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    }

    return context

from decimal import Decimal
from django.conf import settings


def basket_content(request):
    basket_items = []
    total = 0
    count = 0
    basket = request.session.get('basket', {})

    for item_id, specs_in_basket in basket.items():
        for specs, quantity in specs_in_basket['items_by_specs'].items():
            specs = specs.split('-')
            item_id = specs[0]
            name = specs[1]
            size_len = specs[2]
            finish_img = specs[3]
            price = Decimal(specs[4])
            image = specs[5]
            quantity = int(quantity)
            total += quantity * price
            item_total = quantity * price
            count += quantity
            item_in_basket = "-".join(specs)
            basket_items.append({
                'item_id': item_id,
                'name': name,
                'size_len': size_len,
                'finish_img': finish_img,
                'price': price,
                'image': image,
                'item_in_basket': item_in_basket,
                'item_total': item_total,
                'quantity': quantity,

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
        'grand_total': grand_total,
        'test_image': image
    }
    return context

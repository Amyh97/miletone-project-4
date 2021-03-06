from decimal import Decimal
from django.conf import settings


def basket_content(request):
    basket_items = []
    total = 0
    count = 0
    basket = request.session.get('basket', {})

    for item in basket.items():
        item_id = item[0]
        name = item[1].split(',')[0].split(":")[1].replace("'", "")
        image = item[1].split(',')[1].split(":", 1)[1].replace("'", "")
        size_len = item[1].split(',')[2].split(":")[1].replace("'", "")
        finish_img = item[1].split(',')[3].split(":")[1].replace("'", "")
        price = Decimal(item[1].split(',')[4].split(":")[1].replace("'", ""))
        quantity = int(item[1].split(',')[5].split(":")[1].replace("']", "")
                       .replace("'", "").strip())
        orderitem_total = price * quantity
        total += orderitem_total
        count += quantity
        basket_items.append({
            'item_id': item_id,
            'name': name,
            'image': image,
            'size_len': size_len,
            'finish_img': finish_img,
            'price': price,
            'quantity': quantity,
            'orderitem_total': orderitem_total,
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
    }
    return context


def stripe_basket(request):
    stripe_items = []
    total = 0
    count = 0
    basket = request.session.get('basket', {})

    for item in basket.items():
        item_id = item[0]
        price = Decimal(item[1].split(',')[4].split(":")[1].replace("'", ""))
        quantity = int(item[1].split(',')[5].split(":")[1].replace("']", "")
                       .replace("'", "").strip())
        orderitem_total = price * quantity
        total += orderitem_total
        count += quantity
        stripe_items.append({
            'item_id': item_id,
            'price': price,
            'quantity': quantity,
            'orderitem_total': orderitem_total,
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
        'basket_items': stripe_items,
        'total': total,
        'count': count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY,
        'grand_total': grand_total,
    }

    return context

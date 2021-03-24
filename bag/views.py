from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from decimal import Decimal


def bag(request):
    """ a view to return bag content """

    return render(request, 'bag/bag.html')


def basket_item(request, item_id):
    """ a view to add items to a bag based on specs """
    if request.POST:
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        size_len = request.POST.get('size_len')
        finish_img = request.POST.get('finish_img')
        """combine item id, size_len and finish_img to ensure each item
        (product or service) will be treated individually """
        item_id = request.POST.get('id')+size_len+finish_img
        image = request.POST.get('image')
        basket = request.session.get('basket', {})
        redirect_url = request.POST.get('redirect_url')

        keys = ('name', 'image', 'size_len', 'finish_img', 'price', 'quantity')
        values = (name, image, size_len, finish_img, price, quantity)

        specs = '[{}]'.format(', '.join("'{}': '{}'".format(k, v) for k, v in zip(keys, values)))
        # list as dict is not hashable
        if item_id not in list(basket):
            basket[item_id] = specs
            messages.success(request, f'Added {quantity} {name}, {size_len},\
                        {finish_img} to your basket.')
        else:
            # what is alreay in the basket
            current_qty = int(basket[item_id].split(',')[5].split(':')[1].replace("']", "").replace("'", "").strip())
            # ensure the number is increased, not overwritten
            new_qty = str(current_qty + quantity)
            # push new quantity into specs
            new_specs = specs.replace(f"'{current_qty}']'", new_qty)
            basket[item_id] = new_specs
            messages.success(request, f'Added another {quantity} to {name}, {size_len},\
                    {finish_img} to your basket.')

    request.session['basket'] = basket

    return redirect(redirect_url)


def adjust_basket(request, item_id):
    """ a view to allow users to change the quantity from basket"""
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})
    name = basket[item_id].split(',')[0].split(":")[1].replace("'", "")
    image = basket[item_id].split(',')[1].split(":", 1)[1].replace("'", "")
    size_len = basket[item_id].split(',')[2].split(":")[1].replace("'", "")
    finish_img = basket[item_id].split(',')[3].split(":")[1].replace("'", "")
    price = Decimal(basket[item_id].split(',')[4].split(":")[1].replace("'", ""))
    keys = ('name', 'image', 'size_len', 'finish_img', 'price', 'quantity')
    values = (name, image, size_len, finish_img, price, quantity)

    specs = '[{}]'.format(', '.join("'{}': '{}'".format(k, v) for k, v in zip(keys, values)))

    if quantity > 0:
        if item_id in list(basket):
            basket[item_id] = specs
            messages.success(request, f'The quantity of {name}, {size_len},\
                    {finish_img} has been changed to {quantity}.')
    else:
        del basket[item_id]
        messages.warning(request, f'{name} has been\
                        removed from your basket')

    return redirect(reverse('bag'))


def remove_from_basket(request, item_id):
    # Remove a specific product in the shopping cart
    basket = request.session.get('basket', {})
    name = basket[item_id].split(',')[0].split(":")[1].replace("'", "")

    if item_id in list(basket):
        try:
            basket.pop(item_id)
            request.session['basket'] = basket
            messages.warning(request, f'{name} has been\
                            removed from your basket')
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)

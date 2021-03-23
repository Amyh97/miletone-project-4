from django.shortcuts import render, redirect, reverse,\
                        HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import products


def bag(request):
    """ a view to return bag content """

    return render(request, 'bag/bag.html')


def basket_item(request, item_id):
    """ a view to add items to a bag based on specs """
    if request.POST:
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        size_len = request.POST.get('size_len')
        finish_img = request.POST.get('finish_img')
        image = request.POST.get('image')
        basket = request.session.get('basket', {})
        redirect_url = request.POST.get('redirect_url')

        keys = ('name', 'image', 'size_len', 'finish_img', 'price', 'quantity')
        values = (name, image, size_len, finish_img, price, quantity)

        if item_type == 'product':
            basket_products = request.session.get('basket_products', {})
            specs = '[{}]'.format(', '.join("'{}': '{}'".format(k, v) for k, v in zip(keys, values)))
            # list as dict is not hashable
            if item_id not in list(basket_products):
                basket_products[item_id] = specs
                messages.success(request, f'Added {quantity} {name}, {size_len},\
                            {finish_img} to your basket.')
                request.session['basket_products'] = basket_products
            else:
                this_size_len = basket_products[item_id].split(',')[2].split(':')[1].replace("'", "").strip()
                this_finish_img = basket_products[item_id].split(',')[3].split(':')[1].replace("'", "").strip()
                if this_size_len == size_len and this_finish_img == finish_img:
                    # what is alreay in the basket
                    current_qty = int(basket_products[item_id].split(',')[5].split(':')[1].replace("']", "").replace("'", "").strip())
                    # ensure the number is increased, not overwritten
                    new_qty = str(current_qty + quantity)
                    # push new quantity into specs
                    new_specs = specs.replace(f"'{current_qty}']'", new_qty)
                    basket_products[item_id] = new_specs
                    messages.success(request, f'Added another {quantity} to {name}, {size_len},\
                            {finish_img} to your basket.')
                else:
                    # create a more unique id to prevent overwriting other id
                    item_id = item_id+size_len+finish_img
                    specs = '[{}]'.format(', '.join("'{}': '{}'".format(k, v) for k, v in zip(keys, values)))
                    basket_products[item_id] = specs
                    request.session['basket_products'] = basket_products

                    messages.success(request, f'Added {quantity} {name}, {size_len},\
                                {finish_img} to your basket.')
            basket = basket_products
        else:
            print('services will be added later')


    request.session['basket'] = basket

    return redirect(redirect_url)


def adjust_basket(request, item_id):
    print('test')


def remove_from_basket(request, item_id):
    print('test')

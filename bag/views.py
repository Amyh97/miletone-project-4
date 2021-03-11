from django.shortcuts import render, redirect, reverse


def bag(request):
    """ a view to return bag content """

    return render(request, 'bag/bag.html')


def basket_item(request, item_id):
    """ a view to add items to a bag based on specs """
    if request.POST:
        item_id = request.POST.get('id')
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        size_len = request.POST.get('size_len')
        finish_img = request.POST.get('finish_img')
        image = request.POST.get('image')
        basket = request.session.get('basket', {})
        redirect_url = request.POST.get('redirect_url')
        item_in_basket = {}
        to_add = (item_id, name, size_len, finish_img, price, image)
        item_in_basket = "-".join(to_add)

    if item_id in list(basket.keys()):
        if item_in_basket in basket[item_id]['items_by_specs'].keys():
            # add variable accesses the last item in the item_in_basket dict
            add = int(basket[item_id]['items_by_specs'][item_in_basket])
            quantity = add + quantity
            basket[item_id]['items_by_specs'][item_in_basket] += quantity - add

        else:
            """
            assign a more unique id if image is already in basket
            with different specs
            """
            item_id = item_id + size_len + finish_img
            basket[item_id] = {'items_by_specs': {item_in_basket: quantity}}

    else:
        basket[item_id] = {'items_by_specs': {item_in_basket: quantity}}

    request.session['basket'] = basket
    print(basket)

    return redirect(redirect_url)


def adjust_basket(request, item_id):
    """Update quantity of a specific product in the shopping cart"""
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})
    # use for loop so code can be run on each item in basket
    for item_id in basket:
        # each item in basket is 3 dictionaries nested in eachother
        # turn values into list, dictionary containing specs and quantity
        basket_item_id = list(basket[item_id].values())
        # turn item into string so it can be split and manipulated
        dict_string = str(basket_item_id[0])
        # remove quotes from string to tidy for context processor
        remove_quotes = dict_string.replace("'", "")
        # split string at : to get value of key value pair
        split_val = remove_quotes.split(":")[0]
        """ remove remaining curly brace so string matches
        the original val of items_by_specs """
        change_quantity = split_val.replace("{", "")
        basket[item_id]['items_by_specs'][change_quantity] = quantity

    request.session['basket'] = basket
    return redirect(reverse('bag'))

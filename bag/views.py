from django.shortcuts import render, redirect


def bag(request):
    """ a view to return bag content """

    return render(request, 'bag/bag.html')


def basket_item(request, item_id):
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
    return redirect(redirect_url)

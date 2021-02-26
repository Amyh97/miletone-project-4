from django.shortcuts import render, redirect


def bag(request):
    """ a view to return bag content """
    return render(request, 'bag/bag.html')


def add_to_basket(request, item_id):
    """ add items, product or services to the basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # session to store this particular basket
    # get basket or initialise new one if not found
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        # if item is already in basket, add x amount
        basket[item_id] += quantity
    else:
        # if not already in the basket, add it
        basket[item_id] = quantity

    # update session basket
    request.session['basket'] = basket

    print(request.session['basket'])
    # bring users back to where they were
    return(redirect(redirect_url))

from django.shortcuts import render, redirect


def bag(request):
    """ a view to return bag content """
    return render(request, 'bag/bag.html')


def add_to_basket(request, item_id):
    if request.POST:
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        size_len = request.POST.get('size_len')
        finish_img = request.POST.get('finish_img')
        image = request.POST.get('image')
        redirect_url = request.POST.get('redirect_url')
        basket = request.session.get('basket', {})
        basket_item = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'size_len': size_len,
            'finish_img': finish_img,
            'image': image,
        }
        if item_id in list(basket.keys()):
            basket_item = str(basket_item)
            basket[basket_item] += quantity
        else:
            basket_item = str(basket_item)
            basket[basket_item] = quantity

        request.session['basket'] = basket

        return redirect(redirect_url)

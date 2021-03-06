from django.shortcuts import render, redirect


def bag(request):
    """ a view to return bag content """
    return render(request, 'bag/bag.html')


def basket_item(request, item_id):
    if request.POST:
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        size_len = request.POST.get('size_len')
        finish_img = request.POST.get('finish_img')
        image = request.POST.get('image')
        basket = request.session.get('basket', {})
        redirect_url = request.POST.get('redirect_url')
        item = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'size_len': size_len,
            'finish_img': finish_img,
            'image': image,
        }
        if item in list(basket.keys()):
            item = str(item)
            basket[item] += quantity
        else:
            item = str(item)
            basket[item] = quantity

        request.session['basket'] = basket
        return redirect(redirect_url)

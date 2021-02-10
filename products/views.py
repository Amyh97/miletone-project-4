from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import products


# Create your views here.
def products_page(request):
    """ A view to display all images for sale"""

    product = products.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    context = {
        'products': product,
    }

    return render(request, 'products/products.html', context)

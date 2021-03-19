from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import products, sizes, finish, categories
from .forms import ProductForm


# Create your views here.
def products_page(request):
    """ A view to display all images for sale"""
    category = categories.objects.all()
    product = products.objects.all()

    if request.GET:
        if 'CategorySort' in request.GET:
            CategorySort = request.GET['CategorySort']
            # double underscore is common Django syntax for queries
            product = products.objects.filter(category__name=CategorySort)
        else:
            product = products.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(product, 18)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    context = {
        'products': product,
        'categories': category,

    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display the detail of a selected image """
    # pk is first field in json file for products data
    product = get_object_or_404(products, pk=product_id)
    size = sizes.objects.all()
    finishes = finish.objects.all()

    context = {
        'product': product,
        'sizes': size,
        'finishes': finishes,
    }
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ add products to site """
    form = ProductForm()
    template = 'products/add_to_store.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

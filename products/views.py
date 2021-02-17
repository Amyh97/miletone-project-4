from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import products, sizes, finish, categories


# Create your views here.
def products_page(request):
    """ A view to display all images for sale"""
    category = categories.objects.all()
    product = products.objects.all()
    #category_sort = None
    search_product = None

    #if request.GET:
    #if 'category_sort' in request.GET:
    #category = request.GET['category_sort']
    # double underscore is common Django syntax for queries
    search_product = product.filter(category__name__in=category)
    category_sort = category.filter(name__in=category)

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
        'categories': category,
        'current_categories': category_sort,
        'search_product': search_product,
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

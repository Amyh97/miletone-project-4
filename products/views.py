from django.shortcuts import render
from .models import products


# Create your views here.
def products_page(request):
    """ A view to display all images for sale"""

    product = products.objects.all()
    context = {
        'products': product,
    }

    return render(request, 'products/products.html', context)

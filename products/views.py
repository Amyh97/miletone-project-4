from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import products, sizes, finish, categories
from .forms import ProductForm


def products_page(request):
    """ A view to display all images for sale"""
    category = categories.objects.all()
    product = products.objects.all()
    search = None

    if request.GET:
        if 'Category' in request.GET:
            Category = request.GET['Category']
            # double underscore is common Django syntax for queries
            product = products.objects.filter(category__name=Category)
        else:
            product = products.objects.all()

        if 'search' in request.GET:
            search = request.GET['search']
            if not search:
                messages.error(request, "You didn't search anything!")
                return redirect(reverse('products'))

            # unable to shorten line to avoid whitespace error
            query = Q(name__icontains=search) | Q(description__icontains=search)
            product = product.filter(query)

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
        'search': search,

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


@login_required
def add_product(request):
    """ add products to site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can add\
            products to the site')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product has successfully been added\
                to the website.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'There was in error in the form, please\
                double check the data and try again.')
    else:
        form = ProductForm()

    template = 'products/add_to_store.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ edit products on the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can edit\
            products on the site')
        return redirect(reverse('home'))

    product = get_object_or_404(products, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully\
                updated {product.name}!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, f'Could not update {product.name}.\
                Please double check the form and try again.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_item.html'

    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can delete\
            products from the site')
        return redirect(reverse('home'))

    product = get_object_or_404(products, pk=product_id)
    product.delete()
    messages.warning(request, f'{product.name} has been removed\
        from the website')
    return redirect(reverse('products'))

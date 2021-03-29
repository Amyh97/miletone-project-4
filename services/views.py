from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Services, Lengths, Images
from .forms import ServiceForm


def services_page(request):
    """ A view to display all images for sale"""
    services = Services.objects.all()

    context = {
        'services': services,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, service_id):
    """ A view to display the detail of a selected service """
    # pk is first field in json file for products data
    services = get_object_or_404(Services, pk=service_id)
    lengths = Lengths.objects.all()
    images = Images.objects.all()

    context = {
        'service': services,
        'lengths': lengths,
        'images': images,
    }
    return render(request, 'services/services_detail.html', context)


@login_required
def add_service(request):
    """ add servives to site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can add\
            services to the site')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            messages.success(request, 'Service has successfully been added\
                to the website.')
            return redirect(reverse('service_detail', args=[int(service.id)]))
        else:
            messages.error(request, 'There was in error in the form, please\
                double check the data and try again.')
    else:
        form = ServiceForm()

    template = 'services/add_service.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_service(request, service_id):
    """ edit servives on the site """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can edit\
            servives on the site')
        return redirect(reverse('home'))

    service = get_object_or_404(Services, pk=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully\
                updated {service.name}!')
            return redirect(reverse('services_detail', args=[service.id]))
        else:
            messages.error(request, f'Could not update {service.name}.\
                Please double check the form and try again.')
    else:
        form = ServiceForm(instance=service)
        messages.info(request, f'You are editing {service.service}')

    template = 'products/edit_item.html'

    context = {
        'form': form,
        'service': service,
    }

    return render(request, template, context)


@login_required
def delete_service(request, service_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry! Only site admin can delete\
            services from the site')
        return redirect(reverse('home'))

    service = get_object_or_404(Services, pk=service_id)
    service.delete()
    messages.warning(request, f'{service.service} has been removed\
        from the website')
    return redirect(reverse('services'))

from django.shortcuts import render


def bag(request):
    """ a view to return bag content """
    return render(request, 'bag/bag.html')

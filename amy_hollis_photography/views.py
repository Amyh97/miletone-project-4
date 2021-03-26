from django.shortcuts import render


def handler404(request, exception):
    return render(request, 'amy_hollis_photography/404.html', status=404)


def handler500(request):
    return render(request, 'amy_hollis_photography/500.html', status=500)

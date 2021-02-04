from django.shortcuts import render


def profile(request):
    """ display user information """

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)

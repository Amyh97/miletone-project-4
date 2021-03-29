from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings

from .forms import ContactForm


def contact(request):
    if request.method == "GET":
        form = ContactForm()
    # if method is post, submit form
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            print(from_email)
            message = form.cleaned_data['message']
            photographer_email = settings.DEFAULT_FROM_EMAIL
            try:
                send_mail(subject, message, from_email,
                          [photographer_email, ])
                messages.success(request, "Thank you. Your email has been sent.\
                                        I will reply to you as soon as I can.")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            messages.error(request, 'Could not send your email.\
                please double check the form.')

    template = 'contact/email.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

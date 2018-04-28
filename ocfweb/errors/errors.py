from django.shortcuts import render


def http404(request):
    """ Function for rendering the error 404 page. """
    return render(request, 'errors/404.html')

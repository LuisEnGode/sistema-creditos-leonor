from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def htmx_test(request):
    return render(request, "core/partials/htmx_response.html")

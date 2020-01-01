from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
    # It automatically searches for a templates/ dir
    return render(request, 'home.html')
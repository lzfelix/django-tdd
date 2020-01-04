from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')

def view_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'list.html', {
        'items': Item.objects.all()
    })

def new_list(request: HttpRequest) -> HttpResponse:
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/first-list/')

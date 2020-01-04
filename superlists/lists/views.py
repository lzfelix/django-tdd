from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    # It automatically searches for a templates/ dir
    return render(request, 'home.html', {
        'items': Item.objects.all()
    })

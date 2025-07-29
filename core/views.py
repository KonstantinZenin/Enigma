from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

MENU_ITEMS = [
    {
        "name": "Главная страница",
        "url_name": "landing"
    },
    {
    "name": "WAAAGHH!",
    "url_name": "landing"
},
]


def landing(request):
    context = {
        "menu_items": MENU_ITEMS,
    }
    return render(request, "core/landing.html", context=context)

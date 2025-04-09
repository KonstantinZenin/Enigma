from email.policy import HTTP
from django.shortcuts import render
from django.http import HttpResponse


def landing(request):
    # return HttpResponse("Сайт Enigma!")
    return render(request, "base.html")

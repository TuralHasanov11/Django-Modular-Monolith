from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "main/index.html")

@login_required
def protected(request: HttpRequest) -> HttpResponse:
    return HttpResponse("You are logged in")
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from .forms import *
from .models import *
# from .utils import *


def index(request):
    return render(request, 'prometheus/index.html', {"title": "Главная страница"})


def afisha(request):
    events = Events.objects.all()

    context = {
        'events': events,
        "title": "Афиша",
        "cat_selected": 0,
    }
    return render(request, 'prometheus/afisha.html', context=context)


def categories(request):
    return HttpResponse(f'<h1>Афиша по категориям</h1>')


def about(request):
    return render(request, 'prometheus/about.html', {'title': 'О нас'})


def art(request):
    return HttpResponse("Творчество")


def news(request):
    return HttpResponse("Новости")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_event(request, event_slug):
    return HttpResponse(f"Отображение статьи c id = {event_slug}")


def show_category(request, cat_id):
    events = Events.objects.filter(category_id=cat_id)

    # if len(events) == 0:
    #     raise Http404()

    context = {
        'events': events,
        "title": "Афиша",
        "cat_selected": cat_id,
    }
    return render(request, 'prometheus/afisha.html', context=context)
from datetime import datetime
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


def index(request):
    return render(request, 'prometheus/index.html', {"title": "Главная страница"})


class Booking(DetailView):
    model = Booking, Events
    template_name = "prometheus/booking.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Купить")
        return dict(list(context.items()) + list(c_def.items()))


class Afisha(DataMixin, ListView):
    model = Events
    template_name = "prometheus/afisha.html"
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Афиша")
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Events.objects.filter(data__gte=datetime.now())


# def afisha(request):
#     events = Events.objects.all()
#
#     context = {
#         'events': events,
#         "title": "Афиша",
#         "cat_selected": 0,
#     }
#     return render(request, 'prometheus/afisha.html', context=context)


def categories(request):
    return HttpResponse(f'<h1>Афиша по категориям</h1>')


def about(request):
    return render(request, 'prometheus/about.html', {'title': 'О нас'})


def art(request):
    if request.method == 'POST':
        form = FirstLessonForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = FirstLessonForm()
    return render(request, 'prometheus/art.html', {'form': form, 'title': "Записаться на пробное занятие"})


def news(request):
    return render(request, 'prometheus/news.html')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowEvent(DataMixin, DetailView):
    model = Events
    template_name = 'prometheus/event.html'
    slug_url_kwarg = 'event_slug'
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['events']
        c_def = self.get_user_context(title="Афиша")
        return dict(list(context.items()) + list(c_def.items()))


# def show_event(request, event_slug):
#     events = get_object_or_404(Events, slug=event_slug)
#
#     context = {
#         'events': events,
#         "title": events.title,
#         "cat_selected": events.category_id,
#     }
#     return render(request, 'prometheus/event.html', context=context)


class AfishaCategory(DataMixin, ListView):
    model = Events
    template_name = "prometheus/afisha.html"
    context_object_name = 'events'
    allow_empty = False

    def get_queryset(self):
        return Events.objects.filter(category__slug=self.kwargs['cat_slug'], data__gte=datetime.now())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['events'][0].category),
                                      cat_selected=context['events'][0].category_id)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_id):
#     events = Events.objects.filter(category_id=cat_id)
#
#     # if len(events) == 0:
#     #     raise Http404()
#
#     context = {
#         'events': events,
#         "title": "Афиша",
#         "cat_selected": cat_id,
#     }
#     return render(request, 'prometheus/afisha.html', context=context)


class AddEvent(DataMixin, CreateView):
    form_class = AddEventForm
    template_name = 'prometheus/add_event.html'
    success_url = reverse_lazy('afisha')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление события")
        return dict(list(context.items()) + list(c_def.items()))


# def add_event(request):
#     if request.method == 'POST':
#         form = AddEventForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('afisha')
#     else:
#         form = AddEventForm()
#
#     context = {
#         "title": "Добавить событие",
#         "form": form,
#     }
#     return render(request, 'prometheus/add_event.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'prometheus/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'prometheus/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

class NewsUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'prometheus/news.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

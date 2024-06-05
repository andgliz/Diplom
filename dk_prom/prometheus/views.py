from datetime import datetime
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import *
from .models import *
from .utils import *


def index(request):
    return render(request, 'prometheus/index.html', {"title": "Главная страница"})


class MainPage(DataMixin, ListView):
    model = Events
    template_name = "prometheus/index.html"
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Events.objects.filter(data__gte=datetime.now())


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


class ShowEvent(DataMixin, FormMixin, DetailView):
    model = Events
    # TODO: Посмотреть как вставлять дефолт параметры для формы
    #  https://stackoverflow.com/questions/604266/django-set-default-form-values
    form_class = BookingForm
    template_name = 'prometheus/event.html'
    slug_url_kwarg = 'event_slug'
    context_object_name = 'event'
    success_url = reverse_lazy('afisha')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        cur_event = context['event']

        context['title'] = cur_event.title
        context['free_seats'] = self.calculate_free_seats(cur_event)

        c_def = self.get_user_context(title="Афиша")
        return dict(list(context.items()) + list(c_def.items()))

    def calculate_free_seats(self, cur_event):
        space_capacity = cur_event.space.capacity
        event_bookings = Booking.objects.filter(event_id=cur_event.id)

        event_seats_reserved = 0
        for booking in event_bookings:
            event_seats_reserved += booking.seats_reserved

        return space_capacity - event_seats_reserved


def proceed_book(request):
    # TODO: Добавить обработку помимо POST и настроить редирект
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('afisha')


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


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'prometheus/user_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("Вы не имеете доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info_form'] = UserInfoForm(instance=self.request.user)
        context['user_password_form'] = UserPasswordForm(self.request.user)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context

    def post(self, request, *args, **kwargs):
        if 'user_info_form' in request.POST:
            form = UserInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Данные успешно изменены.')
                return redirect('user_profile_settings', form.cleaned_data.get('username'))
            else:
                context = self.get_context_data(**kwargs)
                context['user_info_form'] = form
                return render(request, self.template_name, context)
        elif 'user_password_form' in request.POST:
            form = UserPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменён.')
                return self.get(request, *args, **kwargs)
            else:
                context = self.get_context_data(**kwargs)
                context['user_password_form'] = form
                return render(request, self.template_name, context)
        else:
            return self.get(request, *args, **kwargs)


class UserProfileView(DataMixin, TemplateView):
    template_name = 'prometheus/profile_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['user_profile'] = user
        context['user_book'] = Booking.objects.filter(user=user)
        # context['title'] = f'Профиль пользователя {user}'

        # -------------------------
        user_book = Booking.objects.filter(user=user)[0]
        event_url = user_book.event.get_absolute_url()
        context['event_url'] = event_url
        c_def = self.get_user_context(title=f'Профиль пользователя {user}')
        return dict(list(context.items()) + list(c_def.items()))

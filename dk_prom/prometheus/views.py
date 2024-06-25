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
from django.contrib.messages.views import SuccessMessageMixin

from .forms import *
from .models import *
from .utils import *


class MainPage(DataMixin, ListView):
    model = Events
    template_name = "prometheus/index.html"
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
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


class ShowEvent(DataMixin, SuccessMessageMixin, FormMixin, DetailView):
    model = Events
    form_class = BookingForm
    template_name = 'prometheus/event.html'
    slug_url_kwarg = 'event_slug'
    context_object_name = 'event'
    success_url = reverse_lazy('afisha')
    success_message = "Спасибо за покупку!"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        cur_event = context['event']
        free_seats = self.calculate_free_seats(cur_event)
        is_buy_shown = free_seats > 0
        is_event_free = cur_event.cost == 0

        context['title'] = cur_event.title
        context['free_seats'] = free_seats
        context['is_buy_shown'] = is_buy_shown
        context['is_event_free'] = is_event_free

        c_def = self.get_user_context(title="Афиша")
        return dict(list(context.items()) + list(c_def.items()))

    def get_form(self, form_class=None):
        form = super().get_form()
        free_seats = self.calculate_free_seats(self.object)

        form.fields["event"].initial = self.object
        form.fields["seats_reserved"].widget.attrs.update(
            {'max': free_seats}
        )
        return form

    def calculate_free_seats(self, cur_event):
        space_capacity = cur_event.space.capacity
        event_bookings = Booking.objects.filter(event_id=cur_event.id)

        event_seats_reserved = 0
        for booking in event_bookings:
            event_seats_reserved += booking.seats_reserved

        # количество свободных мест всегда больше или равно 0
        free_seats = max(0, space_capacity - event_seats_reserved)
        return free_seats


def proceed_book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Спасибо за покупку!')
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('afisha')


class AddEvent(DataMixin, CreateView):
    form_class = AddEventForm
    template_name = 'prometheus/add_event.html'
    success_url = reverse_lazy('afisha')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление события")
        return dict(list(context.items()) + list(c_def.items()))


class ArtPage(DataMixin, SuccessMessageMixin, CreateView, ListView):
    model = Groups
    context_object_name = 'group'
    form_class = FirstLessonForm
    template_name = 'prometheus/art.html'
    success_url = reverse_lazy('art')
    success_message = "Ваша заявка успешно отправлена"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Творчество")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class ShowGroup(DataMixin, DetailView):
    model = Groups
    template_name = 'prometheus/group.html'
    slug_url_kwarg = 'group_slug'
    context_object_name = 'group'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Творчество")
        return dict(list(context.items()) + list(c_def.items()))


class NewsPage(DataMixin, ListView):
    model = News
    template_name = "prometheus/news.html"
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Новости")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = News
    template_name = 'prometheus/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Новости")
        return dict(list(context.items()) + list(c_def.items()))


class AddNew(DataMixin, CreateView):
    form_class = AddNewForm
    template_name = 'prometheus/add_new.html'
    success_url = reverse_lazy('news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление новости")
        return dict(list(context.items()) + list(c_def.items()))


class AboutPage(DataMixin, ListView):
    model = Events
    template_name = "prometheus/about.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О нас")
        return dict(list(context.items()) + list(c_def.items()))


def about(request):
    return render(request, 'prometheus/about.html', {'title': 'О нас'})


class RegisterUser(DataMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'prometheus/register.html'
    success_url = reverse_lazy('login')
    success_message = "Регистрация прошла успешно! Добро пожаловать!"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, SuccessMessageMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'prometheus/login.html'
    success_message = "Добро пожаловать!"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


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
        context['user_recover'] = FirstLessons.objects.all()

        user_bookings = Booking.objects.filter(user=user)
        bookings_to_url = list()
        for book in user_bookings:
            event_url = book.event.get_absolute_url()
            bookings_to_url.append((book, event_url))

        context['bookings_to_url'] = bookings_to_url
        c_def = self.get_user_context(title=f'Профиль пользователя {user}')
        return dict(list(context.items()) + list(c_def.items()))


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


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

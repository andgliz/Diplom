from django.db.models import Count

from .models import *

menu = [{'title': "Афиша", 'url_name': 'afisha'},
        {'title': "Творчество", 'url_name': 'art'},
        {'title': "Новости", 'url_name': 'news'},
        {'title': "О нас", 'url_name': 'about'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Categories.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context


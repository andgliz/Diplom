from django import template
from prometheus.models import *

register = template.Library()


@register.inclusion_tag('prometheus/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Categories.objects.all()
    else:
        cats = Categories.objects.order_by(sort)

    return{"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('prometheus/menu.html')
def show_menu(sort=None):
    menu = [{'title': "Афиша", 'url_name': 'afisha'},
            {'title': "Творчество", 'url_name': 'art'},
            {'title': "Новости", 'url_name': 'news'},
            {'title': "О нас", 'url_name': 'about'},
            ]
    return {"menu": menu}

from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('categories/', categories),
    path('afisha/', afisha, name='afisha'),
    # path('', PrometheusHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('news/', news, name='news'),
    path('art/', art, name='art'),
    path('login/', login, name='login'),
    path('category/<int:cat_id>/', show_category, name='category'),
    path('afisha/<slug:event_slug>/', show_event, name='event'),
    #  path('booking/<book:cat_slug>/', PrometheusBooking.as_view(), name='booking'),
]
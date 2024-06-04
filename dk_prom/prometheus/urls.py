from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('categories/', categories),
    path('afisha/', Afisha.as_view(), name='afisha'),
    # path('', PrometheusHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('news/', NewsUser.as_view(), name='news'),
    path('art/', art, name='art'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('book/', proceed_book, name='book'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('afisha/add_event/', AddEvent.as_view(), name='add_event'),
    path('category/<slug:cat_slug>/', AfishaCategory.as_view(), name='category'),
    path('afisha/<slug:event_slug>/', ShowEvent.as_view(), name='event'),
]
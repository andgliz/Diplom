from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('afisha/', Afisha.as_view(), name='afisha'),
    path('about/', about, name='about'),
    path('news/', NewsPage.as_view(), name='news'),
    path('art/', ArtPage.as_view(), name='art'),
    path('art/<slug:group_slug>/', ShowGroup.as_view(), name='group'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('book/', proceed_book, name='book'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('<str:username>/settings/', UserSettingsView.as_view(), name='user_profile_settings'),
    path('afisha/add_event/', AddEvent.as_view(), name='add_event'),
    path('category/<slug:cat_slug>/', AfishaCategory.as_view(), name='category'),
    path('afisha/<slug:event_slug>/', ShowEvent.as_view(), name='event'),
]

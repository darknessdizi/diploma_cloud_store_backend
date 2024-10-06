from django.urls import path
from .views import File, get_csrf, loginUser, registrationUser
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('csrf/', get_csrf, name='csrf'),
    path('registration/', registrationUser, name='registration'),
    path('login/', loginUser, name='login'),
    path('file/', File.as_view(), name='file'),
    path('file/<int:id>', File.as_view(), name='file'),
]
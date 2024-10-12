from django.urls import path
from .views import File, get_csrf, get_files, login_user, registration_user, file_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('csrf/', get_csrf, name='csrf'),
    path('registration/', registration_user, name='registration'),
    path('login/', login_user, name='login'),
    path('getfiles/<int:id>/', get_files, name='allFiles'),
    path('filedata/<int:file_id>/', file_data, name='filedata'),
    path('file/', File.as_view(), name='file'),
    path('file/<int:id>/', File.as_view(), name='newFile'),
]
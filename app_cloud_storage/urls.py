from django.urls import path
from .views import File, get_files, login_user, registration_user, file_data, recovery_session, logout_user, get_link, download_file, get_users, change_status, delete_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('csrf/', get_csrf, name='csrf'),
    path('registration/', registration_user, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('get-files/<int:user_id>/', get_files, name='all_files'),
    path('recovery-session/', recovery_session, name='recovery'),
    path('filedata/<int:file_id>/', file_data, name='filedata'),
    path('file/', File.as_view(), name='file'),
    path('file/<int:id>/', File.as_view(), name='newFile'),
    path('getlink/<int:id>/', get_link, name='get_link'),
    path('download/<str:path>/', download_file, name='download'),
    path('admin/get-users/', get_users, name='all_users'),
    path('admin/change-status/', change_status, name='change_status'),
    path('admin/delete-user/<int:id>/', delete_user, name='delete_user'),
]

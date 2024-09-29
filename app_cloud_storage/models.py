from django.db import models
import secrets

# Модели таблиц для облачного хранилища

# Директория сохранения файлов и аватаров
def user_directory_path(instance, filename):
    try:
        if instance.file:
            return f'user_files/user_{instance.user.id}/{filename}'
    except (Exception, ):
        return f'avatars/user_{instance.user.id}/{secrets.token_hex(12)}'

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    user_login = models.CharField(max_length=20)
    user_full_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=250)
    user_password = models.CharField(max_length=250)
    user_avatar = models.ImageField(upload_to=user_directory_path, default='')
    user_status_admin = models.BooleanField()
    user_created = models.DateTimeField(auto_now_add=True)
    user_last_visit = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_login

class Files(models.Model):
    id = models.IntegerField(primary_key=True)
    file_title = models.CharField(max_length=250)
    file_origin_name = models.CharField(max_length=250)
    file_link = models.CharField(max_length=250)
    file_created = models.DateTimeField(auto_now_add=True)
    file_last_download = models.DateTimeField(null=True, blank=True)
    file_size = models.CharField(max_length=250)
    file_body = models.FileField(upload_to=user_directory_path)
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Файл пользователя'
        verbose_name_plural = 'Файлы пользователей'

# class Permission(models.Model):
#     id = models.IntegerField(primary_key=True)
#     users_id = models.ForeignKey(Users, models.DO_NOTHING, on_delete=models.CASCADE)
#     files_id = models.ForeignKey(Files, models.DO_NOTHING, on_delete=models.CASCADE)


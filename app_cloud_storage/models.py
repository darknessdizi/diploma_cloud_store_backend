from django.db import models
import secrets

# Модели таблиц для облачного хранилища

# Директория сохранения файлов и аватаров
def user_directory_path(instance, filename):
    try:
        if instance.file:
            return f'user_files/user_{instance.user_id.id}/{filename}'
    except (Exception, ):
        return f'avatars/user_{instance.user.id}/{secrets.token_hex(12)}'

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    sex = models.CharField(max_length=5)
    avatar = models.ImageField(upload_to=user_directory_path, default='')
    status_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["full_name"]

    def __str__(self):
        return self.login

    def to_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'full_name': self.full_name,
            'email': self.email,
            'avatar': self.avatar,
            'status_admin': self.status_admin,
            'created': self.created,
            'last_visit': self.last_visit,
        }

class Files(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)
    size = models.CharField(max_length=250)
    file = models.FileField(upload_to=user_directory_path)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment = models.TextField(default='')

    class Meta:
        verbose_name = 'Файл пользователя'
        verbose_name_plural = 'Файлы пользователей'

class UserSession(models.Model):
    session_token = models.CharField(max_length=100, default='')
    created = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


# Generated by Django 5.1.1 on 2024-09-29 14:59

import app_cloud_storage.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_login', models.CharField(max_length=20)),
                ('user_full_name', models.CharField(max_length=100)),
                ('user_email', models.CharField(max_length=250)),
                ('user_password', models.CharField(max_length=250)),
                ('user_avatar', models.ImageField(default='', upload_to=app_cloud_storage.models.user_directory_path)),
                ('user_status_admin', models.BooleanField()),
                ('user_created', models.DateTimeField(auto_now_add=True)),
                ('user_last_visit', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('file_title', models.CharField(max_length=250)),
                ('file_origin_name', models.CharField(max_length=250)),
                ('file_link', models.CharField(max_length=250)),
                ('file_created', models.DateTimeField(auto_now_add=True)),
                ('file_last_download', models.DateTimeField(blank=True, null=True)),
                ('file_size', models.CharField(max_length=250)),
                ('file_body', models.FileField(upload_to=app_cloud_storage.models.user_directory_path)),
                ('users_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_cloud_storage.users')),
            ],
            options={
                'verbose_name': 'Файл пользователя',
                'verbose_name_plural': 'Файлы пользователей',
            },
        ),
    ]

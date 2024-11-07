# Generated by Django 5.1.1 on 2024-11-07 17:26

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('sex', models.CharField(max_length=5)),
                ('avatar', models.ImageField(default='', upload_to=app_cloud_storage.models.user_directory_path)),
                ('status_admin', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_visit', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_download', models.DateTimeField(blank=True, null=True)),
                ('size', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to=app_cloud_storage.models.user_directory_path)),
                ('comment', models.TextField(default='')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_cloud_storage.users')),
            ],
            options={
                'verbose_name': 'Файл пользователя',
                'verbose_name_plural': 'Файлы пользователей',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_token', models.CharField(default='', max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_cloud_storage.users')),
            ],
            options={
                'verbose_name': 'Сессия пользователя',
                'verbose_name_plural': 'Сессии пользователей',
            },
        ),
    ]

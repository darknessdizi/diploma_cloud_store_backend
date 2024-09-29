from django.db import models

class Users(models.Model):
  id = models.IntegerField(primary_key=True)
  user_login = models.CharField(max_length=40)
  user_password = models.CharField(max_length=10)
  status_admin = models.BooleanField()

class Files(models.Model):
  id = models.IntegerField(primary_key=True)
  file_title = models.CharField()
  file_origin_name = models.CharField()
  file_link = models.CharField()

class Permission(models.Model):
  id = models.IntegerField(primary_key=True)
  users_id = models.ForeignKey(Users, models.DO_NOTHING)
  files_id = models.ForeignKey(Files, models.DO_NOTHING)


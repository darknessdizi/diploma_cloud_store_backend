from django.contrib import admin
from .models import Files, Users, UserSession

# Register your models here.
admin.site.register(Files)
admin.site.register(Users)
admin.site.register(UserSession)


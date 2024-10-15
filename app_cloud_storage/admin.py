from django.contrib import admin
from .models import Files, Users, UserSession

# Register your models here.
admin.site.register(Files)
admin.site.register(Users)

class UserSessionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'user_id', ) # если нужно увидеть не отображаемые поля

admin.site.register(UserSession, UserSessionAdmin)

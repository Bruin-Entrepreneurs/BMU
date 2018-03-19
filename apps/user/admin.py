from django.contrib import admin

from apps.user.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    exclude = ['password', ]


admin.site.register(User, UserAdmin)

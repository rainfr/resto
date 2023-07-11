from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)

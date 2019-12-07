from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # 使用django自己的UserAdmin来注册
from django.utils.translation import gettext_lazy
from .models import User


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None,{'fields': ('username', 'password','first_name', 'last_name', 'email')}),

        (gettext_lazy('User Information'), {'fields': ('nickname', 'hosts_permission', 'gtm_permission')}),

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',)}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserProfileAdmin)

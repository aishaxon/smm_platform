from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, Permission, UserPermission


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("username", "phone", "role")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "phone", "role", "is_active_employee", "telegram_id")
    list_filter = ("role", "is_active_employee")

    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone", "role", "password1", "password2"),
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        ("SMM platforma", {"fields": ("phone", "telegram_id", "role", "is_active_employee")}),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "permission")
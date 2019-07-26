from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed "username" field
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "phone_number")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "password1", "password2")}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ("email", "name", "is_staff", "phone_number")
    search_fields = ("email", "name", "phone_number")
    ordering = ("email",)
    readonly_fields = ("date_joined", "last_login")


admin.site.register(User, CustomUserAdmin)

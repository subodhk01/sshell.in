from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

ADDITIONAL_FIELDS = (
        ("User Avatar", {
            "fields": (
                'avatar',
            ),
        }),
    )

class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_FIELDS
    fieldsets =  ADDITIONAL_FIELDS + UserAdmin.fieldsets

admin.site.register(User, CustomUserAdmin)
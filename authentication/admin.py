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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2')
        }),
        ("Permissions", {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active')
        })
    )
    fieldsets =  ADDITIONAL_FIELDS + UserAdmin.fieldsets

admin.site.register(User, CustomUserAdmin)

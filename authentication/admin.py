from django.contrib import admin
from .models import User, RandomToken
from django.contrib.auth.admin import UserAdmin

ADDITIONAL_FIELDS = (
        ("Extra fields", {
            "fields": (
                'avatar',
                'is_verified',
                'last_send_verification_link'
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
            'fields': ('is_verified', 'is_staff', 'is_active', 'last_send_verification_link')
        })
    )
    fieldsets =  ADDITIONAL_FIELDS + UserAdmin.fieldsets

admin.site.register(User, CustomUserAdmin)

@admin.register(RandomToken)	
class RandomTokenAdmin(admin.ModelAdmin):	
    list_display = (	
        'token',	
        'user',	
        'expiry_minutes',
        'created_at',	
        'expires_at'	
    )	
    readonly_fields = (	
        'token',	
        'user',	
        'expiry_minutes',
        'created_at',	
        'expires_at'	
    ) 
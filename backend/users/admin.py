from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'fullname', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    list_display = ('fullname', 'email',  'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
    search_fields = ('fullname','email','groups' )
    ordering = ('fullname','email')

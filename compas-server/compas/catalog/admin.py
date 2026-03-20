# catalog/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Roles

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role',)}),
    )
    # Если хотите, чтобы role было в форме создания:
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Roles)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_name']
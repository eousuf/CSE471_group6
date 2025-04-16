from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Parent

class ParentAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(Parent, ParentAdmin)
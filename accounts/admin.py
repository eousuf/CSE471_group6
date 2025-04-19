from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Parent,Child,Daycare

class ParentAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'daycare', 'phone_number', 'position')
    search_fields = ('full_name', 'phone_number', 'position')

admin.site.register(Parent, ParentAdmin)

class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'daycare', 'age', 'group')
    list_filter = ('daycare', 'group')
    search_fields = ('name',)

admin.site.register(Child, ChildAdmin)


@admin.register(Daycare)
class DaycareAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    search_fields = ('name',)
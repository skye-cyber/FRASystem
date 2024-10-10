# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import ClockIn, CustomUser, Enrollment


# Custom User Admin
class CustormUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'status', 'is_staff')
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'status')}
         ),
    )


# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrolled_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('enrolled_at',)


# ClockIn Admin
class ClockInAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock_in_time')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('clock_in_time',)


# Unregister the default User model
# admin.site.unregister(UserAdmin)
# Register the models with the custom admin classes
admin.site.register(CustomUser, CustormUserAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(ClockIn, ClockInAdmin)

# Optionally unregister the Group model if you're not using it
admin.site.unregister(Group)

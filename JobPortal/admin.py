from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RecruiterProfile, JobseekerProfile, Job, Application

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'display_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'display_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'display_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RecruiterProfile)
admin.site.register(JobseekerProfile)
admin.site.register(Job)
admin.site.register(Application)
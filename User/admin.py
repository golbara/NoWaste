from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyAuthor

class UserAdmin(BaseUserAdmin):
    # Use the email field as the username field in the admin interface
    ordering = ['email']
    list_display = ['email', 'is_active', 'is_staff']
    list_filter = ['email','password']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    filter_horizontal = ()
    
    def save_model(self, request, obj, form, change):
        # Hash the password before saving the user model
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(MyAuthor, UserAdmin)

# class UserAdmin(BaseUserAdmin):
#     pass
# admin.site.register(MyAuthor, UserAdmin)
# admin.site.register(MyAuthor)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(VC_Codes)

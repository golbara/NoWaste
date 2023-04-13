from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import *

# class AccountAdmin(UserAdmin):
#     pass


# admin.site.register(MyAuthor, AccountAdmin)

# @admin.register(MyAuthor)
# class UserAdmin(BaseUserAdmin):
#     pass
# admin.site.register(MyAuthor, UserAdmin)
# admin.site.register(MyAuthor)
admin.site.register(Customer)
admin.site.register(Restaurant)

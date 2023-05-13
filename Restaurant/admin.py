from django.contrib import admin
from .models import Food
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'restaurant', 'Type']
    list_filter = ['Type','restaurant']
    search_fields = ('name','Type')
admin.site.register(Food,FoodAdmin)
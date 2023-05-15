from django.contrib import admin
from .models import *
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'restaurant', 'type']
    list_filter = ['type','restaurant']
    search_fields = ('name','type')
admin.site.register(Food,FoodAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)


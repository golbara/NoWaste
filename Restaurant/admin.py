from django.contrib import admin
from .models import *
# Register your models here.

class FoodAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'restaurant', 'type']
    list_filter = ['type','restaurant']
    search_fields = ('name','type')

class OrderAdmin(admin.ModelAdmin):
    ordering = ['created_at', 'userId']
    list_display = ['id', 'userId', 'restaurant', 'status']
    list_filter = ['status','restaurant', 'userId']
    search_fields = ('id',)

class OrderItemAdmin(admin.ModelAdmin):
    ordering = ['quantity']
    list_display = ['food', 'order']
    list_filter = ['order', 'food','quantity']
    # search_fields = (,)
admin.site.register(Food,FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)


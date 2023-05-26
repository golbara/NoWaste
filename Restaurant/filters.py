from django_filters.rest_framework import FilterSet
from .models import *

class RestaurantFilter(FilterSet):
  class Meta:
    model = Restaurant
    fields = {
        # 'collection_id': ['exact'],
        'type': ['exact'],
        'rate': ['gte', 'lte'],
        'discount': ['gte', 'lte'],
    }

class FoodFilter(FilterSet):
  class Meta:
    model = Food
    fields = {
        'type': ['exact'],
        'price': ['gte', 'lte'],
    }
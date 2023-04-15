from django.urls import path, include
from .views import *
# from rest_framework import routers
# from rest_framework_nested import routers

# router = routers.DefaultRouter()
# router.register('restaurant', RestaurantView, basename='restaurant')


# products_router = routers.NestedSimpleRouter(router, 'restaurant', lookup='restaurant')
# products_router.register('food', FoodViewSet, basename='restaurant-food')

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='restaurant_change_password'),
    path('Restaurant_profile/<int:id>/', RestaurantView.as_view(), name='restaurant-profile'),
]
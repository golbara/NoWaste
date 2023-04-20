from django.urls import path, include
from .views import *
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
# router.register('restaurant-view', RestaurantView, basename='restaurant')
router.register('restaurant-search', RestaurantSearchViewSet, basename='restaurant-search')

# products_router = routers.NestedSimpleRouter(router, 'restaurant', lookup='restaurant')
# products_router.register('food', FoodViewSet, basename='restaurant-food')

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='restaurant_change_password'),
    path('restaurant_profile/<int:id>/', RestaurantView.as_view(), name='restaurant-profile'),
    path('', include(router.urls)),
]
# urlpatterns = router.urls


from django.urls import path, include
from .views import *
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('restaurant-search', RestaurantSearchViewSet, basename='restaurant-search')
router.register('restaurant_profile',RestaurantProfileViewSet,basename = 'rest-profile')
router.register('filter-food', FilterFoodViewSet, basename='filter-food')
# router.register('order', OrderViewSet)

router.register('restaurant_view', RestaurantCustomerView, basename='restaurant')
order_router = routers.NestedSimpleRouter(router, 'restaurant_view', lookup='restaurant')
order_router.register('order', OrderViewSet , basename='order')

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_view', lookup='restaurant')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(order_router.urls)),
    path('managers/<int:pk>/', RestaurantManagerDetailView.as_view(), name='manager-detail'),
    path('managers/<int:manager_id>/restaurants/', RestaurantManagerRestaurantListView.as_view(), name='restaurant-list'),
    path('managers/<int:manager_id>/restaurants/<int:pk>/', RestaurantManagerRestaurantDetailView.as_view(), name='restaurant-detail'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/', ManagerFoodAPIView.as_view(), name='food-list'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/<int:pk>/',  ManagerFoodViewSet.as_view(), name='food-detail')
]




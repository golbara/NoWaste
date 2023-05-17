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
# order_router = routers.NestedSimpleRouter(router, 'restaurant_view', lookup='restaurant')
# order_router.register('order', OrderViewSet , basename='order')

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_view', lookup='restaurant')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')


urlpatterns = [
    path(r'', include(router.urls)),
    # path(r'', include(order_router.urls)),
    path('restaurant_view/<int:restaurant_id>/<int:userId>/order/',OrderAPIView.as_view(), name = 'order-detail'),
    path('restaurant_view/<int:restaurant_id>/order/<uuid:order_id>/<int:food_id>/add_to_order/',add_to_Order, name = 'add-to-order'),
    path('restaurant_view/<int:restaurant_id>/order/<uuid:order_id>/<int:food_id>/remove_from_order/',remove_from_Order, name = 'add-to-order'),
    path('managers/<int:pk>/', RestaurantManagerDetailView.as_view(), name='manager-detail'),
    path('managers/<int:manager_id>/restaurants/', RestaurantManagerRestaurantListView.as_view(), name='restaurant-list'),
    path('managers/<int:manager_id>/restaurants/<int:pk>/', RestaurantManagerRestaurantDetailView.as_view(), name='restaurant-detail'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/', ManagerFoodListCreateAPIView.as_view(), name='food-list'),
    path('managers/<int:manager_id>/restaurants/<int:restaurant_id>/food/<int:pk>/',  ManagerFoodViewSet.as_view(), name='food-detail')
]




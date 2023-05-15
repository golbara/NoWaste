from django.urls import path, include
from .views import *
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('restaurant_view', RestaurantCustomerView, basename='restaurant')
router.register('restaurant-search', RestaurantSearchViewSet, basename='restaurant-search')
router.register('restaurant_profile',RestaurantProfileViewSet,basename = 'rest-profile')
router.register('filter-food', FilterFoodViewSet, basename='filter-food')

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_profile', lookup='id')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='restaurant_change_password'),
    # path('restaurant_view/<int:id>/', RestaurantView.as_view(), name='restaurant-view'),
    # path('restaurant_profile/<int:id>/', RestaurantView.as_view(), name='restaurant-profile'),
    # path('restaurant_customer_view/', RestaurantCustomerView.as_view({'get': 'list'}), name='restaurant-view'),
    path(r'', include(router.urls)),
    # path('managers/', RestaurantManagerListCreateView.as_view(), name='manager-list'),
    # path('managers/<int:pk>/', RestaurantManagerRetrieveUpdateDestroyView.as_view(), name='manager-detail'),

    path('managers/<int:pk>/', RestaurantManagerDetailView.as_view(), name='manager-detail'),
    path('managers/<int:manager_id>/restaurants/', RestaurantManagerRestaurantListView.as_view(), name='restaurant-list'),
    path('managers/<int:manager_id>/restaurants/<int:pk>/', RestaurantManagerRestaurantDetailView.as_view(), name='restaurant-detail'),
]
# urlpatterns = router.urls



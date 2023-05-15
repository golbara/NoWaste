from django.urls import path, include
from .views import *
# from rest_framework import routers
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('restaurant_view', RestaurantCustomerView, basename='restaurant')
router.register('restaurant-search', RestaurantSearchViewSet, basename='restaurant-search')
router.register('restaurant_profile',RestaurantProfileViewSet,basename = 'rest-profile')
# router.register('order', OrderViewSet)

restaurant_router = routers.NestedSimpleRouter(router, 'restaurant_profile', lookup='id')
restaurant_router.register('food', FoodViewSet, basename='restaurant-food')

order_router = routers.NestedSimpleRouter(router, 'restaurant_profile', lookup='id')
order_router.register('order', OrderViewSet , basename='order')

urlpatterns = [
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('order/', OrderViewSet, name='watch-order'),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='restaurant_change_password'),
    # path('restaurant_view/<int:id>/', RestaurantView.as_view(), name='restaurant-view'),
    # path('restaurant_profile/<int:id>/', RestaurantView.as_view(), name='restaurant-profile'),
    # path('restaurant_customer_view/', RestaurantCustomerView.as_view({'get': 'list'}), name='restaurant-view'),
    path(r'', include(router.urls)),
]
# urlpatterns = router.urls



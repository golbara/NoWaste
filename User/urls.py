from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'update_profile', UpdateProfileView, basename='update_profile')
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('editProfile/', CustomerViewSet.as_view(), name='editpro'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordViewSet.as_view(), name='forgot-password'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='Customer_change_password'),
    # path('update_profile/', UpdateProfileView.as_view({'get': 'list'}), name='Customer_update_profile'),
    # path('', include(router.urls)),
     path('update_profile/', UpdateProfileView.as_view(), name='update-profile'),
    # path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='Customer_update_profile'),


]
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('editProfile/', CustomerViewSet.as_view(), name='editpro'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordViewSet.as_view(), name='forgot-password'),

]
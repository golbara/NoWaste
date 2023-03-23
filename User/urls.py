from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('auth/', obtain_auth_token),
    path('login/', LoginView.as_view(), name='login'),
]
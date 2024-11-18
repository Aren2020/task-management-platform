from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.RegistrationAPIView.as_view(), name = 'signup'),
    path('login/', views.LoginAPIView.as_view(), name = 'login'),
    path('logout/', views.LogoutAPIView.as_view(), name = 'logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
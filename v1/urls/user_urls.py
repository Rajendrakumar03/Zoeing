from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from v1.views.user_views import RegisterView, LoginView, LogoutView, MeView,CustomTokenObtainPairView



user_urlpatterns =[
    path('auth/register', RegisterView.as_view(),name='register'),
    path('auth/login',LoginView.as_view(),name='login'),
    path('auth/logout',LogoutView.as_view(),name='logout'),
    path('auth/refresh',TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me',MeView.as_view(), name='me'),
    path('auth/token',CustomTokenObtainPairView.as_view(),name='token')
]
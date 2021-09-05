from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import login_view, logout_view, register_view, get_auth_key, get_csrf, SessionView

urlpatterns = [
  path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
  path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
  path('login', login_view, name='login'),
  path('logout', logout_view, name='logout'),
  path('register', register_view, name='register'),
  path('get_auth_key', get_auth_key, name='get_auth_key'),
  path('get_csrf', get_csrf, name='get_csrf'),
  path('session', SessionView.as_view(), name='session'),
]
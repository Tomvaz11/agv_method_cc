"""
URL configuration for IABANK project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Create a router and register our viewsets with it
router = DefaultRouter()

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API base
    path('api/v1/', include(router.urls)),
    
    # Authentication endpoints
    path('api/v1/auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),
    
    # Health check endpoint
    path('health/', include('iabank.core.urls')),
    
    # App URLs
    path('api/v1/users/', include('iabank.users.urls')),
    path('api/v1/customers/', include('iabank.customers.urls')),
    path('api/v1/operations/', include('iabank.operations.urls')),
    path('api/v1/finance/', include('iabank.finance.urls')),
]
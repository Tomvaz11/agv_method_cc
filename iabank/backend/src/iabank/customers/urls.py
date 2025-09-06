"""
URL configuration for customers app.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import CustomerViewSet

router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]

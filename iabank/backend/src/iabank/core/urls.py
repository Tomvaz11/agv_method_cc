"""
URL configuration for core app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health-check'),
    path('ready/', views.ready_check, name='ready-check'),
]
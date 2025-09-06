"""
Tests for core views - Health check endpoint validation.
"""
import json

from django.test import Client, TestCase
from rest_framework import status


class TestHealthCheckView(TestCase):
    """Test health check endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_health_check_endpoint(self):
        """Test that health check endpoint returns proper response."""
        response = self.client.get('/health/')

        assert response.status_code == status.HTTP_200_OK

        data = json.loads(response.content)
        assert 'status' in data
        assert 'timestamp' in data
        assert 'services' in data
        assert 'version' in data

        # Check that database service is included
        assert 'database' in data['services']
        assert data['services']['database']['status'] == 'healthy'

    def test_ready_check_endpoint(self):
        """Test that ready check endpoint works."""
        response = self.client.get('/health/ready/')

        assert response.status_code == status.HTTP_200_OK

        data = json.loads(response.content)
        assert data['status'] == 'ready'
        assert 'timestamp' in data

    def test_health_check_no_auth_required(self):
        """Test that health check doesn't require authentication."""
        # This should work without any authentication headers
        response = self.client.get('/health/')
        assert response.status_code == status.HTTP_200_OK

    def test_ready_check_no_auth_required(self):
        """Test that ready check doesn't require authentication."""
        # This should work without any authentication headers
        response = self.client.get('/health/ready/')
        assert response.status_code == status.HTTP_200_OK

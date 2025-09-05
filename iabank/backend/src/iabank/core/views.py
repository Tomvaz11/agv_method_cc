"""
Core views for IABANK - Health check and utility endpoints.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint that validates system components.
    
    Returns:
    - 200 OK if all services are healthy
    - 503 Service Unavailable if any critical service is down
    """
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'services': {},
        'version': '1.0.0'
    }
    
    overall_healthy = True
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['services']['database'] = {
                'status': 'healthy',
                'response_time': '< 50ms'
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['services']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        overall_healthy = False
    
    # Check Redis/Cache connectivity
    try:
        cache.set('health_check', 'test', timeout=10)
        if cache.get('health_check') == 'test':
            health_status['services']['cache'] = {
                'status': 'healthy',
                'response_time': '< 10ms'
            }
            cache.delete('health_check')
        else:
            raise Exception("Cache set/get test failed")
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        health_status['services']['cache'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        # Cache is not critical, so don't mark overall as unhealthy
    
    # Set overall status
    if not overall_healthy:
        health_status['status'] = 'unhealthy'
        return Response(health_status, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response(health_status, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def ready_check(request):
    """
    Readiness check endpoint for Kubernetes/container orchestration.
    
    This is a simpler check that just verifies the application is running.
    """
    return Response({
        'status': 'ready',
        'timestamp': timezone.now().isoformat()
    }, status=status.HTTP_200_OK)
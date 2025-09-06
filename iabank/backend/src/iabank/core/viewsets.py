"""
Base viewsets for IABANK - Foundation DNA for API endpoints.

This module provides base viewset classes that establish consistent
patterns for API endpoints, permissions, and tenant isolation.
"""
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base viewset that provides common functionality for all API endpoints.

    Features:
    - Consistent permission handling
    - Standard error responses
    - Common filtering and pagination
    - Audit logging
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """
        Add request context to serializer.
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def handle_exception(self, exc):
        """
        Provide consistent error handling across all endpoints.
        """
        if isinstance(exc, ValidationError):
            return Response(
                {'error': 'Dados inválidos', 'details': exc.message_dict},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)

    def perform_create(self, serializer):
        """
        Add common create logic (like setting tenant).
        """
        # The serializer handles tenant assignment automatically
        serializer.save()

    def perform_update(self, serializer):
        """
        Add common update logic.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle deletion with proper validation.
        """
        # Check if instance can be safely deleted
        if hasattr(instance, 'can_be_deleted') and not instance.can_be_deleted():
            raise ValidationError("Este registro não pode ser excluído pois está sendo utilizado.")
        instance.delete()


class BaseTenantViewSet(BaseViewSet):
    """
    ViewSet for models that inherit from BaseTenantModel.

    Automatically filters querysets by tenant and provides
    tenant-specific functionality.
    """

    def get_queryset(self):
        """
        Filter queryset by user's tenant.
        """
        if not hasattr(self.request.user, 'tenant'):
            return self.queryset.none()

        base_queryset = super().get_queryset()
        if isinstance(base_queryset, QuerySet):
            return base_queryset.filter(tenant=self.request.user.tenant)
        return base_queryset

    def perform_create(self, serializer):
        """
        Ensure tenant is set correctly on creation.
        """
        if hasattr(self.request.user, 'tenant'):
            serializer.save(tenant=self.request.user.tenant)
        else:
            raise ValidationError("Usuário não possui tenant associado.")

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Common endpoint to get statistics for the model.
        Override in subclasses to provide specific stats.
        """
        queryset = self.get_queryset()
        total = queryset.count()

        return Response({
            'total': total,
            'model': self.queryset.model.__name__,
            'timestamp': timezone.now().isoformat()
        })


class ReadOnlyTenantViewSet(BaseTenantViewSet):
    """
    Read-only viewset for tenant models.
    Useful for reference data that shouldn't be modified via API.
    """

    def create(self, request, *args, **kwargs):
        return Response(
            {'error': 'Operação não permitida'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Operação não permitida'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Operação não permitida'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Operação não permitida'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

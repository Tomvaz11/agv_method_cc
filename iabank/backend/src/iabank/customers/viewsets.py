"""
Customer viewsets for IABANK - Customer management API endpoints.

This module demonstrates complete ViewSet implementation following
the established DNA patterns from the core app.
"""
from django.db.models import Count, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from iabank.core.viewsets import BaseTenantViewSet

from .models import Customer
from .serializers import (
    CustomerCreateSerializer,
    CustomerListSerializer,
    CustomerSearchSerializer,
    CustomerSerializer,
    CustomerStatsSerializer,
    CustomerUpdateSerializer,
)


class CustomerViewSet(BaseTenantViewSet):
    """
    ViewSet for customer management within tenant.

    Demonstrates complete CRUD operations with:
    - Tenant isolation
    - Custom actions
    - Search functionality
    - Statistics endpoints
    - Proper permission handling
    """

    model = Customer
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'city', 'state']
    search_fields = ['name', 'document_number', 'email']
    ordering_fields = ['name', 'created_at', 'document_number']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get customers for current tenant with optimizations.
        """
        queryset = super().get_queryset()

        # Optimize queries with annotations
        queryset = queryset.annotate(
            has_active_loans=Count(
                'loans',
                filter=Q(loans__status='IN_PROGRESS')
            ) > 0,
            active_loans_count=Count(
                'loans',
                filter=Q(loans__status='IN_PROGRESS')
            )
        )

        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CustomerUpdateSerializer
        elif self.action == 'list':
            return CustomerListSerializer
        elif self.action in ['search', 'search_results']:
            return CustomerListSerializer
        return CustomerSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search customers by name, document, or email.
        """
        serializer = CustomerSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data['query']
        active_only = serializer.validated_data['active_only']
        with_loans_only = serializer.validated_data['with_loans_only']

        # Get base queryset
        queryset = self.get_queryset()

        # Apply search
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(document_number__icontains=query) |
            Q(email__icontains=query)
        )

        # Apply filters
        if active_only:
            queryset = queryset.filter(is_active=True)

        if with_loans_only:
            queryset = queryset.filter(active_loans_count__gt=0)

        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get list of active customers.
        """
        queryset = self.get_queryset().filter(is_active=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomerListSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = CustomerListSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_loans(self, request):
        """
        Get customers with active loans.
        """
        queryset = self.get_queryset().filter(active_loans_count__gt=0)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomerListSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = CustomerListSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a customer.
        """
        customer = self.get_object()
        customer.is_active = True
        customer.save()

        return Response({
            'message': f'Cliente {customer.name} ativado com sucesso.'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a customer (if they have no active loans).
        """
        customer = self.get_object()

        if customer.has_active_loans():
            return Response({
                'error': 'Não é possível desativar cliente com empréstimos ativos.'
            }, status=status.HTTP_400_BAD_REQUEST)

        customer.is_active = False
        customer.save()

        return Response({
            'message': f'Cliente {customer.name} desativado com sucesso.'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get customer statistics for the tenant.
        """
        queryset = self.get_queryset()

        # Calculate date for "this month"
        now = timezone.now()
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        stats = {
            'total_customers': queryset.count(),
            'active_customers': queryset.filter(is_active=True).count(),
            'customers_with_loans': queryset.filter(active_loans_count__gt=0).count(),
            'new_customers_this_month': queryset.filter(
                created_at__gte=first_day_of_month
            ).count(),
            'timestamp': now
        }

        serializer = CustomerStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def loans(self, request, pk=None):
        """
        Get loans for a specific customer.
        This is a placeholder that will be fully implemented when loans app is created.
        """
        customer = self.get_object()

        # For now, return a simple response
        # This will be enhanced when the loans app is implemented
        return Response({
            'customer_id': customer.id,
            'customer_name': customer.name,
            'active_loans_count': customer.get_active_loans_count(),
            'message': 'Loans endpoint will be fully implemented with the loans app.'
        })

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to prevent deletion of customers with loans.
        """
        customer = self.get_object()

        if not customer.can_be_deleted():
            return Response({
                'error': 'Não é possível excluir cliente que possui empréstimos.'
            }, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)

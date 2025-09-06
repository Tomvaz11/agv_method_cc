"""
Customer serializers for IABANK - Customer data serialization.

This module demonstrates the complete implementation of serializers
following the established DNA patterns from the core app.
"""
from rest_framework import serializers

from iabank.core.serializers import BaseTenantSerializer

from .models import Customer


class CustomerSerializer(BaseTenantSerializer):
    """
    Main serializer for Customer model.
    Demonstrates complete CRUD serialization patterns.
    """

    # Computed fields for API responses
    formatted_document = serializers.CharField(source='get_formatted_document', read_only=True)
    formatted_phone = serializers.CharField(source='get_formatted_phone', read_only=True)
    full_address = serializers.CharField(source='get_full_address', read_only=True)
    has_active_loans = serializers.BooleanField(read_only=True)
    active_loans_count = serializers.IntegerField(source='get_active_loans_count', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'document_number', 'birth_date',
            'email', 'phone', 'zip_code', 'street', 'number',
            'complement', 'neighborhood', 'city', 'state',
            'is_active', 'notes', 'created_at', 'updated_at',
            # Computed fields
            'formatted_document', 'formatted_phone', 'full_address',
            'has_active_loans', 'active_loans_count'
        ]
        read_only_fields = (
            'id', 'created_at', 'updated_at',
            'formatted_document', 'formatted_phone', 'full_address',
            'has_active_loans', 'active_loans_count'
        )

    def validate_document_number(self, value):
        """
        Validate document number (CPF/CNPJ).
        """
        if not value:
            raise serializers.ValidationError("Documento é obrigatório.")

        # Remove all non-numeric characters for validation
        numbers = ''.join(filter(str.isdigit, value))

        # Basic length validation
        if len(numbers) not in [11, 14]:
            raise serializers.ValidationError(
                "Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)."
            )

        # Check uniqueness within tenant
        tenant = None
        if hasattr(self.context.get('request', {}), 'user'):
            user = self.context['request'].user
            if user.is_authenticated and hasattr(user, 'tenant'):
                tenant = user.tenant

        if tenant:
            existing_customer = Customer.objects.filter(
                tenant=tenant,
                document_number=value
            ).exclude(pk=self.instance.pk if self.instance else None).first()

            if existing_customer:
                raise serializers.ValidationError(
                    "Já existe um cliente com este documento neste tenant."
                )

        return value

    def validate_email(self, value):
        """
        Validate email uniqueness within tenant if provided.
        """
        if not value:
            return value

        tenant = None
        if hasattr(self.context.get('request', {}), 'user'):
            user = self.context['request'].user
            if user.is_authenticated and hasattr(user, 'tenant'):
                tenant = user.tenant

        if tenant:
            existing_customer = Customer.objects.filter(
                tenant=tenant,
                email=value
            ).exclude(pk=self.instance.pk if self.instance else None).first()

            if existing_customer:
                raise serializers.ValidationError(
                    "Já existe um cliente com este e-mail neste tenant."
                )

        return value

    def validate_zip_code(self, value):
        """
        Validate Brazilian ZIP code format.
        """
        if not value:
            return value

        # Remove all non-numeric characters
        numbers = ''.join(filter(str.isdigit, value))

        if len(numbers) != 8:
            raise serializers.ValidationError(
                "CEP deve conter 8 dígitos."
            )

        return value


class CustomerCreateSerializer(CustomerSerializer):
    """
    Serializer for creating new customers.
    Includes additional validations for required fields.
    """

    def validate(self, attrs):
        """
        Additional validation for customer creation.
        """
        attrs = super().validate(attrs)

        # Ensure required fields are provided
        if not attrs.get('name'):
            raise serializers.ValidationError({
                'name': 'Nome é obrigatório.'
            })

        if not attrs.get('document_number'):
            raise serializers.ValidationError({
                'document_number': 'Documento é obrigatório.'
            })

        return attrs


class CustomerListSerializer(CustomerSerializer):
    """
    Lightweight serializer for customer list views.
    Excludes heavy fields for better performance.
    """

    class Meta(CustomerSerializer.Meta):
        fields = [
            'id', 'name', 'document_number', 'email', 'phone',
            'city', 'state', 'is_active', 'created_at',
            # Computed fields
            'formatted_document', 'formatted_phone',
            'has_active_loans', 'active_loans_count'
        ]


class CustomerUpdateSerializer(CustomerSerializer):
    """
    Serializer for updating customer information.
    Allows partial updates and excludes immutable fields.
    """

    def validate(self, attrs):
        """
        Validation for customer updates.
        """
        attrs = super().validate(attrs)

        # Don't allow deactivating customers with active loans
        if 'is_active' in attrs and not attrs['is_active']:
            if self.instance and self.instance.has_active_loans():
                raise serializers.ValidationError({
                    'is_active': 'Não é possível desativar cliente com empréstimos ativos.'
                })

        return attrs


class CustomerSearchSerializer(serializers.Serializer):
    """
    Serializer for customer search parameters.
    """
    query = serializers.CharField(
        required=True,
        min_length=3,
        help_text="Termo de busca (nome, documento ou email)"
    )

    active_only = serializers.BooleanField(
        default=True,
        help_text="Buscar apenas clientes ativos"
    )

    with_loans_only = serializers.BooleanField(
        default=False,
        help_text="Buscar apenas clientes com empréstimos"
    )


class CustomerStatsSerializer(serializers.Serializer):
    """
    Serializer for customer statistics.
    """
    total_customers = serializers.IntegerField()
    active_customers = serializers.IntegerField()
    customers_with_loans = serializers.IntegerField()
    new_customers_this_month = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

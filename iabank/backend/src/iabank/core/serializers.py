"""
Base serializers for IABANK - Foundation DNA for DRF serialization.

This module provides base serializer classes that establish consistent
patterns for data validation, transformation, and tenant isolation.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tenant


User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """
    Base serializer that provides common functionality for all serializers.
    
    Features:
    - Automatic tenant handling
    - Common field configurations
    - Standardized error messages
    - Audit field handling
    """
    
    # Exclude audit fields from write operations by default
    read_only_fields = ('id', 'created_at', 'updated_at')
    
    class Meta:
        abstract = True
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide tenant field from API consumers - it's handled internally
        if 'tenant' in self.fields:
            self.fields['tenant'].write_only = True
    
    def validate(self, attrs):
        """
        Base validation that ensures tenant consistency.
        """
        attrs = super().validate(attrs)
        
        # Add tenant from request context if creating a new instance
        if not self.instance and hasattr(self.context.get('request', {}), 'user'):
            user = self.context['request'].user
            if user.is_authenticated and hasattr(user, 'tenant'):
                attrs['tenant'] = user.tenant
        
        return attrs
    
    def to_representation(self, instance):
        """
        Custom representation that handles common formatting.
        """
        data = super().to_representation(instance)
        
        # Format datetime fields consistently
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.DateTimeField) and field_name in data:
                if data[field_name]:
                    # Format as ISO string for frontend consumption
                    data[field_name] = instance.__dict__[field_name].isoformat() if hasattr(instance.__dict__[field_name], 'isoformat') else data[field_name]
        
        return data


class BaseTenantSerializer(BaseSerializer):
    """
    Serializer for models that inherit from BaseTenantModel.
    
    Automatically handles tenant isolation and provides
    additional tenant-specific validations.
    """
    
    def validate(self, attrs):
        """
        Ensure tenant consistency for tenant-aware models.
        """
        attrs = super().validate(attrs)
        
        # Validate that all foreign keys belong to the same tenant
        request = self.context.get('request')
        if request and hasattr(request.user, 'tenant'):
            user_tenant = request.user.tenant
            
            for field_name, value in attrs.items():
                field = self.fields.get(field_name)
                if (isinstance(field, serializers.PrimaryKeyRelatedField) and 
                    hasattr(value, 'tenant') and value.tenant != user_tenant):
                    raise serializers.ValidationError({
                        field_name: f"O registro selecionado não pertence ao seu tenant."
                    })
        
        return attrs


class TenantSerializer(BaseSerializer):
    """
    Serializer for Tenant model.
    """
    
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ('id', 'created_at', 'updated_at')


class HealthCheckSerializer(serializers.Serializer):
    """
    Serializer for health check endpoint.
    """
    status = serializers.CharField()
    timestamp = serializers.DateTimeField()
    services = serializers.DictField()
    version = serializers.CharField()
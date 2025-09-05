"""
User serializers for IABANK - Authentication and user data serialization.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from iabank.core.serializers import BaseSerializer
from iabank.core.models import Tenant

User = get_user_model()


class UserSerializer(BaseSerializer):
    """
    Serializer for User model.
    Provides safe user data serialization for API responses.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    full_name_or_username = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone', 'is_active', 'display_name', 'full_name_or_username',
            'tenant_name', 'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'last_login', 
            'tenant_name', 'display_name', 'full_name_or_username'
        )
    
    def validate_email(self, value):
        """
        Validate that email is unique within the tenant.
        """
        if value:
            user = self.context['request'].user
            existing_user = User.objects.filter(
                tenant=user.tenant,
                email=value
            ).exclude(pk=self.instance.pk if self.instance else None).first()
            
            if existing_user:
                raise serializers.ValidationError(
                    "Já existe um usuário com este email neste tenant."
                )
        return value
    
    def validate_username(self, value):
        """
        Validate that username is unique within the tenant.
        """
        user = self.context['request'].user
        existing_user = User.objects.filter(
            tenant=user.tenant,
            username=value
        ).exclude(pk=self.instance.pk if self.instance else None).first()
        
        if existing_user:
            raise serializers.ValidationError(
                "Já existe um usuário com este nome de usuário neste tenant."
            )
        return value


class UserCreateSerializer(UserSerializer):
    """
    Serializer for creating new users.
    Includes password handling and additional validations.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password', 'password_confirm']
    
    def validate(self, attrs):
        """
        Validate password confirmation.
        """
        attrs = super().validate(attrs)
        
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'As senhas não coincidem.'
            })
        
        # Remove password_confirm from validated data
        attrs.pop('password_confirm', None)
        return attrs
    
    def create(self, validated_data):
        """
        Create user with encrypted password.
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(UserSerializer):
    """
    Serializer for updating user information.
    Excludes sensitive fields that shouldn't be changed via API.
    """
    
    class Meta(UserSerializer.Meta):
        fields = [
            'first_name', 'last_name', 'email', 'phone'
        ]
    

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change functionality.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_current_password(self, value):
        """
        Validate that current password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value
    
    def validate(self, attrs):
        """
        Validate that new passwords match.
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'As senhas não coincidem.'
            })
        return attrs


class UserProfileSerializer(UserSerializer):
    """
    Serializer for user profile view.
    Includes additional computed fields for profile display.
    """
    permissions = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['permissions']
    
    def get_permissions(self, obj):
        """
        Get user permissions for frontend display.
        """
        return {
            'is_staff': obj.is_staff,
            'is_superuser': obj.is_superuser,
            'is_active': obj.is_active,
        }
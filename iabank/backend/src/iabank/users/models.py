"""
User models for IABANK - Custom user implementation with tenant support.

This module implements the custom User model that integrates with the
multi-tenant architecture established in the core app.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from iabank.core.models import Tenant, BaseModelMixin


class User(AbstractUser, BaseModelMixin):
    """
    Custom User model that extends Django's AbstractUser with tenant support.
    
    This model establishes the foundation for multi-tenant user management,
    ensuring that all users belong to a specific tenant.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Tenant"
    )
    
    # Additional user fields
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['-created_at']
        
        # Ensure username is unique within tenant
        unique_together = [('tenant', 'username')]
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.tenant.name})"
    
    def get_display_name(self):
        """
        Return a user-friendly display name.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
    
    def can_access_tenant(self, tenant):
        """
        Check if user can access a specific tenant.
        Currently, users can only access their own tenant.
        """
        return self.tenant == tenant
    
    def is_in_same_tenant(self, other_user):
        """
        Check if this user is in the same tenant as another user.
        """
        return self.tenant == other_user.tenant
    
    @property
    def full_name_or_username(self):
        """
        Return full name if available, otherwise username.
        """
        full_name = self.get_full_name()
        return full_name if full_name else self.username
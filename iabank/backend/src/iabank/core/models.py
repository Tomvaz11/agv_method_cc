"""
Core models for IABANK - Base classes and Tenant system.

This module contains the foundation models that establish the DNA
of the project architecture, including multi-tenancy support.
"""
from django.db import models
from django.utils import timezone


class Tenant(models.Model):
    """
    Tenant model for multi-tenant architecture.
    Each tenant represents an isolated instance of the application.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class BaseTenantModel(models.Model):
    """
    Abstract base model for all tenant-aware models.

    This ensures that all data is isolated by tenant,
    establishing the foundation for multi-tenant architecture.

    All models that inherit from this will automatically:
    - Have tenant isolation
    - Include audit fields (created_at, updated_at)
    - Follow consistent naming patterns
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
        verbose_name="Tenant"
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
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        Override save to ensure proper tenant handling.
        """
        # Ensure updated_at is always set
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class BaseManager(models.Manager):
    """
    Base manager that provides tenant-aware queries.
    """

    def for_tenant(self, tenant):
        """
        Filter queryset by tenant.
        """
        return self.filter(tenant=tenant)

    def active(self):
        """
        Filter to only active records (if the model has is_active field).
        """
        if hasattr(self.model, 'is_active'):
            return self.filter(is_active=True)
        return self.all()


class BaseModelMixin:
    """
    Mixin that provides common functionality for all models.
    """

    def refresh_from_db_with_select_related(self, fields=None, **kwargs):
        """
        Refresh from database with optimized select_related.
        """
        if hasattr(self, 'select_related_fields'):
            kwargs.setdefault('fields', fields)
            db_instance = (
                self.__class__.objects
                .select_related(*self.select_related_fields)
                .get(pk=self.pk)
            )
            for field in self._meta.get_fields():
                if field.name in self.select_related_fields:
                    setattr(self, field.name, getattr(db_instance, field.name))
        else:
            super().refresh_from_db(fields=fields, **kwargs)

    def to_dict(self):
        """
        Convert model instance to dictionary.
        Useful for serialization and debugging.
        """
        data = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if isinstance(value, models.Model):
                data[field.name] = str(value)
            elif hasattr(value, 'isoformat'):  # datetime objects
                data[field.name] = value.isoformat()
            else:
                data[field.name] = value
        return data

"""
Tests for core models - Foundation DNA validation.

These tests validate the base architecture components and ensure
the tenant isolation works correctly.
"""
from django.db import models
from django.test import TestCase
from django.utils import timezone

from ..models import BaseModelMixin, BaseTenantModel, Tenant


class TestTenant(TestCase):
    """Test the Tenant model functionality."""

    def test_create_tenant(self):
        """Test creating a new tenant."""
        tenant = Tenant.objects.create(name="Test Tenant")

        assert tenant.id is not None
        assert tenant.name == "Test Tenant"
        assert tenant.is_active is True
        assert tenant.created_at is not None
        assert tenant.updated_at is not None
        assert str(tenant) == "Test Tenant"

    def test_tenant_timestamps(self):
        """Test that timestamps are automatically set."""
        before_create = timezone.now()
        tenant = Tenant.objects.create(name="Timestamp Test")
        after_create = timezone.now()

        assert before_create <= tenant.created_at <= after_create
        assert before_create <= tenant.updated_at <= after_create

    def test_tenant_update_timestamp(self):
        """Test that updated_at is modified on save."""
        tenant = Tenant.objects.create(name="Update Test")
        original_updated = tenant.updated_at

        # Wait a moment to ensure timestamp difference
        import time
        time.sleep(0.001)

        tenant.name = "Updated Name"
        tenant.save()

        assert tenant.updated_at > original_updated


class MockTenantModel(BaseTenantModel, BaseModelMixin):
    """Mock model for testing BaseTenantModel functionality."""
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'core'


class TestBaseTenantModel(TestCase):
    """Test the BaseTenantModel abstract base class."""

    def setUp(self):
        """Set up test data."""
        self.tenant = Tenant.objects.create(name="Test Tenant")

    def test_base_tenant_model_creation(self):
        """Test creating a model that inherits from BaseTenantModel."""
        mock_model = MockTenantModel.objects.create(
            name="Test Model",
            tenant=self.tenant
        )

        assert mock_model.id is not None
        assert mock_model.tenant == self.tenant
        assert mock_model.created_at is not None
        assert mock_model.updated_at is not None

    def test_tenant_isolation(self):
        """Test that models are properly isolated by tenant."""
        tenant2 = Tenant.objects.create(name="Second Tenant")

        model1 = MockTenantModel.objects.create(
            name="Model 1",
            tenant=self.tenant
        )
        model2 = MockTenantModel.objects.create(
            name="Model 2",
            tenant=tenant2
        )

        # Filter by tenant should only return models for that tenant
        tenant1_models = MockTenantModel.objects.filter(tenant=self.tenant)
        tenant2_models = MockTenantModel.objects.filter(tenant=tenant2)

        assert model1 in tenant1_models
        assert model1 not in tenant2_models
        assert model2 in tenant2_models
        assert model2 not in tenant1_models

    def test_cascade_delete(self):
        """Test that deleting a tenant cascades to related models."""
        mock_model = MockTenantModel.objects.create(
            name="Test Model",
            tenant=self.tenant
        )

        self.tenant.delete()

        # The model should be deleted due to CASCADE
        assert not MockTenantModel.objects.filter(id=mock_model.id).exists()

    def test_model_save_override(self):
        """Test that the save override works correctly."""
        mock_model = MockTenantModel(name="Test Model", tenant=self.tenant)

        # Before save, updated_at might not be set
        before_save = timezone.now()
        mock_model.save()
        after_save = timezone.now()

        assert before_save <= mock_model.updated_at <= after_save

    def test_to_dict_method(self):
        """Test the to_dict utility method."""
        mock_model = MockTenantModel.objects.create(
            name="Test Model",
            tenant=self.tenant
        )

        model_dict = mock_model.to_dict()

        assert isinstance(model_dict, dict)
        assert 'id' in model_dict
        assert 'name' in model_dict
        assert 'tenant' in model_dict
        assert 'created_at' in model_dict
        assert 'updated_at' in model_dict

        # Check that datetime fields are properly formatted
        assert isinstance(model_dict['created_at'], str)
        assert isinstance(model_dict['updated_at'], str)

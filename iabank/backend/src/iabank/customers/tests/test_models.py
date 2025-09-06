"""
Tests for customer models - Foundation DNA validation.

These tests validate the complete implementation of domain models
following the established architectural patterns.
"""
import pytest
from django.db import IntegrityError
from django.test import TestCase

from ..models import Customer
from .factories import CustomerFactory, CustomerWithCNPJFactory, TenantFactory


class TestCustomerModel(TestCase):
    """Test the Customer model functionality."""

    def setUp(self):
        """Set up test data."""
        self.tenant = TenantFactory()
        self.other_tenant = TenantFactory()

    def test_create_customer(self):
        """Test creating a new customer."""
        customer = CustomerFactory(tenant=self.tenant)

        assert customer.id is not None
        assert customer.tenant == self.tenant
        assert customer.name is not None
        assert customer.document_number is not None
        assert customer.is_active is True
        assert customer.created_at is not None
        assert customer.updated_at is not None

    def test_customer_string_representation(self):
        """Test customer string representation."""
        customer = CustomerFactory(
            tenant=self.tenant,
            name="João Silva",
            document_number="12345678900"
        )

        assert str(customer) == "João Silva - 12345678900"

    def test_unique_document_within_tenant(self):
        """Test that document number is unique within tenant."""
        document = "12345678900"

        # Create first customer
        CustomerFactory(tenant=self.tenant, document_number=document)

        # Try to create another customer with same document in same tenant
        with pytest.raises(IntegrityError):
            CustomerFactory(tenant=self.tenant, document_number=document)

    def test_same_document_different_tenants_allowed(self):
        """Test that same document can exist in different tenants."""
        document = "12345678900"

        customer1 = CustomerFactory(tenant=self.tenant, document_number=document)
        customer2 = CustomerFactory(tenant=self.other_tenant, document_number=document)

        assert customer1.document_number == customer2.document_number
        assert customer1.tenant != customer2.tenant

    def test_get_formatted_document_cpf(self):
        """Test CPF formatting."""
        customer = CustomerFactory(
            tenant=self.tenant,
            document_number="12345678901"
        )

        formatted = customer.get_formatted_document()
        assert formatted == "123.456.789-01"

    def test_get_formatted_document_cnpj(self):
        """Test CNPJ formatting."""
        customer = CustomerWithCNPJFactory(
            tenant=self.tenant,
            document_number="12345678000123"
        )

        formatted = customer.get_formatted_document()
        assert formatted == "12.345.678/0001-23"

    def test_get_formatted_phone(self):
        """Test phone formatting."""
        customer = CustomerFactory(
            tenant=self.tenant,
            phone="11987654321"
        )

        formatted = customer.get_formatted_phone()
        assert formatted == "(11) 98765-4321"

    def test_get_full_address(self):
        """Test full address formatting."""
        customer = CustomerFactory(
            tenant=self.tenant,
            street="Rua das Flores",
            number="123",
            complement="Apto 45",
            neighborhood="Centro",
            city="São Paulo",
            state="SP"
        )

        full_address = customer.get_full_address()
        expected = "Rua das Flores, 123, Apto 45, Centro, São Paulo, SP"
        assert full_address == expected

    def test_get_full_address_partial(self):
        """Test full address with partial data."""
        customer = CustomerFactory(
            tenant=self.tenant,
            street="Rua das Flores",
            number="123",
            complement=None,
            neighborhood="Centro",
            city="São Paulo",
            state="SP"
        )

        full_address = customer.get_full_address()
        expected = "Rua das Flores, 123, Centro, São Paulo, SP"
        assert full_address == expected

    def test_has_active_loans_false(self):
        """Test has_active_loans when customer has no loans."""
        customer = CustomerFactory(tenant=self.tenant)

        assert customer.has_active_loans() is False
        assert customer.get_active_loans_count() == 0

    def test_can_be_deleted_without_loans(self):
        """Test that customer without loans can be deleted."""
        customer = CustomerFactory(tenant=self.tenant)

        assert customer.can_be_deleted() is True

    def test_to_dict_method(self):
        """Test the enhanced to_dict method."""
        customer = CustomerFactory(tenant=self.tenant)

        customer_dict = customer.to_dict()

        assert isinstance(customer_dict, dict)
        assert 'id' in customer_dict
        assert 'name' in customer_dict
        assert 'formatted_document' in customer_dict
        assert 'formatted_phone' in customer_dict
        assert 'full_address' in customer_dict
        assert 'has_active_loans' in customer_dict
        assert 'active_loans_count' in customer_dict

    def test_customer_manager_for_tenant(self):
        """Test custom manager tenant filtering."""
        customer1 = CustomerFactory(tenant=self.tenant)
        customer2 = CustomerFactory(tenant=self.other_tenant)

        tenant_customers = Customer.objects.for_tenant(self.tenant)

        assert customer1 in tenant_customers
        assert customer2 not in tenant_customers

    def test_customer_manager_active_for_tenant(self):
        """Test custom manager active filtering."""
        active_customer = CustomerFactory(tenant=self.tenant, is_active=True)
        inactive_customer = CustomerFactory(tenant=self.tenant, is_active=False)

        active_customers = Customer.objects.active_for_tenant(self.tenant)

        assert active_customer in active_customers
        assert inactive_customer not in active_customers

    def test_customer_manager_search(self):
        """Test custom manager search functionality."""
        customer1 = CustomerFactory(tenant=self.tenant, name="João Silva")
        customer2 = CustomerFactory(tenant=self.tenant, name="Maria Santos")
        customer3 = CustomerFactory(tenant=self.tenant, email="joao@test.com")

        # Search by name
        results = Customer.objects.search("João", self.tenant)
        assert customer1 in results
        assert customer2 not in results

        # Search by email
        results = Customer.objects.search("joao@test.com", self.tenant)
        assert customer3 in results
        assert customer2 not in results

    def test_tenant_isolation_in_manager(self):
        """Test that manager methods respect tenant isolation."""
        customer1 = CustomerFactory(tenant=self.tenant, name="João Silva")
        customer2 = CustomerFactory(tenant=self.other_tenant, name="João Silva")

        # Search should only return customers from the specified tenant
        results = Customer.objects.search("João", self.tenant)
        assert customer1 in results
        assert customer2 not in results

        results_other = Customer.objects.search("João", self.other_tenant)
        assert customer2 in results_other
        assert customer1 not in results_other

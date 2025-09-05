"""
Factories for customer tests - Foundation DNA for test data generation.

This module demonstrates how to create proper test factories
following the established patterns for the multi-tenant architecture.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model
from iabank.core.models import Tenant
from ..models import Customer

fake = Faker('pt_BR')
User = get_user_model()


class TenantFactory(DjangoModelFactory):
    """
    Factory for creating Tenant instances.
    """
    class Meta:
        model = Tenant
    
    name = factory.LazyAttribute(lambda obj: fake.company())
    is_active = True


class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances with tenant association.
    """
    class Meta:
        model = User
    
    username = factory.LazyAttribute(lambda obj: fake.user_name())
    email = factory.LazyAttribute(lambda obj: fake.email())
    first_name = factory.LazyAttribute(lambda obj: fake.first_name())
    last_name = factory.LazyAttribute(lambda obj: fake.last_name())
    phone = factory.LazyAttribute(lambda obj: fake.phone_number())
    is_active = True
    tenant = factory.SubFactory(TenantFactory)
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        
        password = extracted or 'testpass123'
        self.set_password(password)
        self.save()


class CustomerFactory(DjangoModelFactory):
    """
    Factory for creating Customer instances.
    Demonstrates proper tenant-aware factory patterns.
    """
    class Meta:
        model = Customer
    
    # Basic Information
    name = factory.LazyAttribute(lambda obj: fake.name())
    document_number = factory.LazyAttribute(lambda obj: fake.cpf().replace('.', '').replace('-', ''))
    birth_date = factory.LazyAttribute(lambda obj: fake.date_of_birth(minimum_age=18, maximum_age=80))
    
    # Contact Information
    email = factory.LazyAttribute(lambda obj: fake.email())
    phone = factory.LazyAttribute(lambda obj: fake.phone_number())
    
    # Address Information
    zip_code = factory.LazyAttribute(lambda obj: fake.postcode())
    street = factory.LazyAttribute(lambda obj: fake.street_name())
    number = factory.LazyAttribute(lambda obj: str(fake.building_number()))
    neighborhood = factory.LazyAttribute(lambda obj: fake.neighborhood())
    city = factory.LazyAttribute(lambda obj: fake.city())
    state = factory.LazyAttribute(lambda obj: fake.state_abbr())
    
    # Status
    is_active = True
    
    # Tenant relationship
    tenant = factory.SubFactory(TenantFactory)
    
    @classmethod
    def create_for_tenant(cls, tenant, **kwargs):
        """
        Create a customer for a specific tenant.
        This method demonstrates the pattern for creating tenant-aware test data.
        """
        kwargs['tenant'] = tenant
        return cls.create(**kwargs)
    
    @classmethod
    def create_batch_for_tenant(cls, size, tenant, **kwargs):
        """
        Create multiple customers for a specific tenant.
        """
        kwargs['tenant'] = tenant
        return cls.create_batch(size, **kwargs)


class CustomerWithoutEmailFactory(CustomerFactory):
    """
    Factory for customers without email.
    Demonstrates factory inheritance patterns.
    """
    email = None


class CustomerWithCNPJFactory(CustomerFactory):
    """
    Factory for corporate customers with CNPJ.
    """
    document_number = factory.LazyAttribute(lambda obj: fake.cnpj().replace('.', '').replace('/', '').replace('-', ''))
    name = factory.LazyAttribute(lambda obj: fake.company())


class InactiveCustomerFactory(CustomerFactory):
    """
    Factory for inactive customers.
    """
    is_active = False
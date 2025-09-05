"""
Customer models for IABANK - Customer management implementation.

This module provides a complete example of how to implement domain models
following the established DNA patterns from the core app.
"""
from django.db import models
from django.core.validators import RegexValidator
from iabank.core.models import BaseTenantModel, BaseManager, BaseModelMixin


class CustomerManager(BaseManager):
    """
    Custom manager for Customer model with tenant-aware methods.
    """
    
    def active_for_tenant(self, tenant):
        """
        Get active customers for a specific tenant.
        """
        return self.for_tenant(tenant).filter(is_active=True)
    
    def with_active_loans(self, tenant=None):
        """
        Get customers with active loans.
        """
        queryset = self.get_queryset()
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        
        return queryset.filter(
            loans__status='IN_PROGRESS'
        ).distinct()
    
    def search(self, query, tenant=None):
        """
        Search customers by name or document number.
        """
        queryset = self.get_queryset()
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        
        return queryset.filter(
            models.Q(name__icontains=query) |
            models.Q(document_number__icontains=query) |
            models.Q(email__icontains=query)
        )


class Customer(BaseTenantModel, BaseModelMixin):
    """
    Customer model - Example of complete domain model implementation.
    
    This serves as a template showing how to:
    - Inherit from BaseTenantModel
    - Use custom managers
    - Implement business logic methods
    - Follow consistent field patterns
    """
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        verbose_name="Nome Completo",
        help_text="Nome completo do cliente"
    )
    
    document_number = models.CharField(
        max_length=20,
        verbose_name="CPF/CNPJ",
        help_text="CPF ou CNPJ do cliente",
        validators=[
            RegexValidator(
                regex=r'^[\d.-]+$',
                message="Documento deve conter apenas números, pontos e traços"
            )
        ]
    )
    
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data de Nascimento"
    )
    
    # Contact Information
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name="E-mail"
    )
    
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Telefone",
        validators=[
            RegexValidator(
                regex=r'^[\d\s\-\(\)\+]+$',
                message="Telefone deve conter apenas números, espaços, parênteses, traços e +"
            )
        ]
    )
    
    # Address Information
    zip_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="CEP"
    )
    
    street = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Logradouro"
    )
    
    number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Número"
    )
    
    complement = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Complemento"
    )
    
    neighborhood = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Bairro"
    )
    
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Cidade"
    )
    
    state = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name="Estado",
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
            ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
            ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ]
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    # Notes
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações",
        help_text="Observações gerais sobre o cliente"
    )
    
    # Custom manager
    objects = CustomerManager()
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']
        
        # Ensure document_number is unique within tenant
        unique_together = [('tenant', 'document_number')]
        
        indexes = [
            models.Index(fields=['tenant', 'document_number']),
            models.Index(fields=['tenant', 'name']),
            models.Index(fields=['tenant', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.document_number}"
    
    def get_full_address(self):
        """
        Return formatted full address.
        """
        address_parts = [
            self.street,
            self.number,
            self.complement,
            self.neighborhood,
            self.city,
            self.state
        ]
        
        # Filter out None/empty values and join
        address = ", ".join([part for part in address_parts if part])
        return address if address else None
    
    def get_formatted_document(self):
        """
        Return formatted document number (CPF/CNPJ).
        """
        if not self.document_number:
            return ""
        
        # Remove all non-numeric characters
        numbers = ''.join(filter(str.isdigit, self.document_number))
        
        if len(numbers) == 11:  # CPF
            return f"{numbers[:3]}.{numbers[3:6]}.{numbers[6:9]}-{numbers[9:]}"
        elif len(numbers) == 14:  # CNPJ
            return f"{numbers[:2]}.{numbers[2:5]}.{numbers[5:8]}/{numbers[8:12]}-{numbers[12:]}"
        else:
            return self.document_number
    
    def get_formatted_phone(self):
        """
        Return formatted phone number.
        """
        if not self.phone:
            return ""
        
        # Remove all non-numeric characters
        numbers = ''.join(filter(str.isdigit, self.phone))
        
        if len(numbers) == 11:  # Mobile with area code
            return f"({numbers[:2]}) {numbers[2:7]}-{numbers[7:]}"
        elif len(numbers) == 10:  # Landline with area code
            return f"({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}"
        else:
            return self.phone
    
    def has_active_loans(self):
        """
        Check if customer has active loans.
        """
        # TODO: Implement when loans model is created
        # return self.loans.filter(status='IN_PROGRESS').exists()
        return False
    
    def get_active_loans_count(self):
        """
        Get count of active loans.
        """
        # TODO: Implement when loans model is created
        # return self.loans.filter(status='IN_PROGRESS').count()
        return 0
    
    def can_be_deleted(self):
        """
        Check if customer can be safely deleted.
        Override from BaseModelMixin.
        """
        # TODO: Implement when loans model is created
        # return not self.loans.exists()
        return True
    
    def to_dict(self):
        """
        Enhanced to_dict that includes computed fields.
        """
        data = super().to_dict()
        data.update({
            'formatted_document': self.get_formatted_document(),
            'formatted_phone': self.get_formatted_phone(),
            'full_address': self.get_full_address(),
            'has_active_loans': self.has_active_loans(),
            'active_loans_count': self.get_active_loans_count(),
        })
        return data
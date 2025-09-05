"""
Admin configuration for customers app.
"""
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.
    """
    list_display = (
        'name', 'document_number', 'email', 'phone', 
        'city', 'state', 'tenant', 'is_active', 'created_at'
    )
    
    list_filter = (
        'tenant', 'is_active', 'state', 'city', 'created_at'
    )
    
    search_fields = (
        'name', 'document_number', 'email', 'phone'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'document_number', 'birth_date', 'tenant')
        }),
        ('Contato', {
            'fields': ('email', 'phone')
        }),
        ('Endereço', {
            'fields': (
                'zip_code', 'street', 'number', 'complement',
                'neighborhood', 'city', 'state'
            ),
            'classes': ('collapse',)
        }),
        ('Status e Observações', {
            'fields': ('is_active', 'notes')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Filter customers by user's tenant for non-superusers.
        """
        qs = super().get_queryset(request)
        
        if not request.user.is_superuser:
            qs = qs.filter(tenant=request.user.tenant)
        
        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Customize form based on user permissions.
        """
        form = super().get_form(request, obj, **kwargs)
        
        if not request.user.is_superuser and 'tenant' in form.base_fields:
            # Limit tenant choices to current user's tenant
            form.base_fields['tenant'].queryset = form.base_fields['tenant'].queryset.filter(
                id=request.user.tenant.id
            )
        
        return form
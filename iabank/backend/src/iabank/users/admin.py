"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for custom User model.
    """
    # Fields to display in the user list
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'tenant', 'is_active', 'is_staff', 'date_joined'
    )

    # Filters for the user list
    list_filter = (
        'tenant', 'is_staff', 'is_superuser', 'is_active',
        'date_joined', 'last_login'
    )

    # Fields to search
    search_fields = ('username', 'email', 'first_name', 'last_name', 'tenant__name')

    # Ordering
    ordering = ('-date_joined',)

    # Fields to display in the user edit form
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('username', 'password')
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Tenant', {
            'fields': ('tenant',)
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Fields for adding a new user
    add_fieldsets = (
        ('Informações Básicas', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Informações Pessoais', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone'),
        }),
        ('Tenant', {
            'classes': ('wide',),
            'fields': ('tenant',),
        }),
        ('Permissões', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff'),
        }),
    )

    # Read-only fields
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')

    def get_form(self, request, obj=None, **kwargs):
        """
        Override to ensure superusers can see all tenants,
        but regular staff can only see their own tenant.
        """
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser and 'tenant' in form.base_fields:
            # Limit tenant choices to current user's tenant
            form.base_fields['tenant'].queryset = form.base_fields['tenant'].queryset.filter(
                id=request.user.tenant.id
            )

        return form

    def get_queryset(self, request):
        """
        Override to show only users from the current user's tenant
        for non-superusers.
        """
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(tenant=request.user.tenant)

        return qs

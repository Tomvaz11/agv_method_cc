"""
Management command to seed foundation data for development and testing.

This command creates sample tenants, users, and customers to validate
the Foundation DNA implementation.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from iabank.core.models import Tenant

User = get_user_model()


class Command(BaseCommand):
    """
    Seed foundation data command.
    
    Creates sample data to validate the multi-tenant architecture
    and Foundation DNA patterns.
    """
    help = 'Seed foundation data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tenants',
            type=int,
            default=2,
            help='Number of tenants to create (default: 2)'
        )
        parser.add_argument(
            '--users-per-tenant',
            type=int,
            default=3,
            help='Number of users per tenant (default: 3)'
        )
        parser.add_argument(
            '--customers-per-tenant',
            type=int,
            default=10,
            help='Number of customers per tenant (default: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        """Execute the command."""
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        with transaction.atomic():
            tenants_created = self.create_tenants(options['tenants'])
            users_created = self.create_users(tenants_created, options['users_per_tenant'])
            customers_created = self.create_customers(tenants_created, options['customers_per_tenant'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Foundation data seeded successfully!\n'
                f'- Created {len(tenants_created)} tenants\n'
                f'- Created {users_created} users\n'
                f'- Created {customers_created} customers'
            )
        )
    
    def clear_data(self):
        """Clear existing test data."""
        # Only clear non-superuser data
        User.objects.filter(is_superuser=False).delete()
        Tenant.objects.all().delete()
        
        self.stdout.write('Existing data cleared.')
    
    def create_tenants(self, count):
        """Create sample tenants."""
        tenants = []
        tenant_names = [
            'ACME Financeira',
            'Beta Crédito',
            'Gamma Capital',
            'Delta Investimentos',
            'Epsilon Finance'
        ]
        
        for i in range(count):
            name = tenant_names[i % len(tenant_names)]
            if count > len(tenant_names):
                name = f"{name} {i + 1}"
            
            tenant, created = Tenant.objects.get_or_create(
                name=name,
                defaults={'is_active': True}
            )
            
            if created:
                tenants.append(tenant)
                self.stdout.write(f'Created tenant: {tenant.name}')
        
        return tenants
    
    def create_users(self, tenants, users_per_tenant):
        """Create sample users for each tenant."""
        total_users = 0
        
        user_data = [
            ('admin', 'Administrador', 'Sistema', 'admin@iabank.com', True, True),
            ('gestor', 'Gestor', 'Principal', 'gestor@iabank.com', True, False),
            ('consultor', 'Consultor', 'Vendas', 'consultor@iabank.com', False, False),
        ]
        
        for tenant in tenants:
            self.stdout.write(f'Creating users for tenant: {tenant.name}')
            
            for i in range(users_per_tenant):
                if i < len(user_data):
                    username, first_name, last_name, email, is_staff, is_superuser = user_data[i]
                    # Make email unique per tenant
                    email = email.replace('@', f'.{tenant.name.lower().replace(" ", "")}@')
                else:
                    # Generate additional users if needed
                    username = f'usuario{i+1}'
                    first_name = f'Usuário'
                    last_name = f'{i+1}'
                    email = f'usuario{i+1}.{tenant.name.lower().replace(" ", "")}@iabank.com'
                    is_staff = False
                    is_superuser = False
                
                # Make username unique per tenant
                full_username = f'{username}.{tenant.name.lower().replace(" ", "")}'
                
                user, created = User.objects.get_or_create(
                    username=full_username,
                    tenant=tenant,
                    defaults={
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'is_staff': is_staff,
                        'is_superuser': is_superuser,
                        'is_active': True,
                    }
                )
                
                if created:
                    user.set_password('iabank123')
                    user.save()
                    total_users += 1
                    self.stdout.write(f'  Created user: {user.username} ({user.email})')
        
        return total_users
    
    def create_customers(self, tenants, customers_per_tenant):
        """Create sample customers for each tenant."""
        try:
            from iabank.customers.tests.factories import CustomerFactory
        except ImportError:
            self.stdout.write(
                self.style.WARNING(
                    'CustomerFactory not available. Skipping customer creation. '
                    'This will be available when the customers app is fully implemented.'
                )
            )
            return 0
        
        total_customers = 0
        
        for tenant in tenants:
            self.stdout.write(f'Creating customers for tenant: {tenant.name}')
            
            customers = CustomerFactory.create_batch_for_tenant(
                size=customers_per_tenant,
                tenant=tenant
            )
            
            total_customers += len(customers)
            self.stdout.write(f'  Created {len(customers)} customers')
        
        return total_customers
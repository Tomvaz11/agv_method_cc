"""
User viewsets for IABANK - User management API endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from iabank.core.viewsets import BaseViewSet
from .serializers import (
    UserSerializer,
    UserCreateSerializer, 
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer
)

User = get_user_model()


class UserViewSet(BaseViewSet):
    """
    ViewSet for user management within tenant.
    
    Provides CRUD operations for users, ensuring tenant isolation
    and appropriate permission handling.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return users for the authenticated user's tenant only.
        """
        if not hasattr(self.request.user, 'tenant'):
            return User.objects.none()
        
        return User.objects.filter(tenant=self.request.user.tenant)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'profile':
            return UserProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        """
        Create user with the same tenant as the requesting user.
        """
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        Get current user's profile information.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """
        Update current user's profile information.
        """
        serializer = UserUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated profile
        profile_serializer = UserProfileSerializer(
            request.user,
            context=self.get_serializer_context()
        )
        return Response(profile_serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change current user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Change password
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Senha alterada com sucesso.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a user account.
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        
        return Response({
            'message': f'Usuário {user.username} ativado com sucesso.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a user account.
        """
        user = self.get_object()
        
        # Prevent users from deactivating themselves
        if user == request.user:
            return Response({
                'error': 'Você não pode desativar sua própria conta.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()
        
        return Response({
            'message': f'Usuário {user.username} desativado com sucesso.'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def active_users(self, request):
        """
        Get list of active users in the tenant.
        """
        active_users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to prevent deletion of current user.
        """
        user = self.get_object()
        
        if user == request.user:
            return Response({
                'error': 'Você não pode excluir sua própria conta.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return super().destroy(request, *args, **kwargs)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SaunaUser, AufgussSession, ChatMessage
from .serializers import UserSerializer, AufgussSerializer, ChatMessageSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Benutzerdefinierte Berechtigung: Nur Admins dürfen schreiben
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff

class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admins to edit it.
    Assumes the model instance has a `created_by` attribute.
    Read-only for authenticated users.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions are only allowed to the owner of the snippet or admin users.
        if not request.user.is_authenticated: # Should be caught by view-level permission
            return False
        return obj.created_by == request.user.saunauser or request.user.is_staff

class IsSenderOrAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow sender of a message or admins to edit/delete it.
    Assumes the model instance has a `sender` attribute.
    Read-only for authenticated users.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        if not request.user.is_authenticated:
            return False
        return obj.sender == request.user.saunauser or request.user.is_staff

class AufgussViewSet(viewsets.ModelViewSet):
    queryset = AufgussSession.objects.select_related('created_by').all()
    serializer_class = AufgussSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly] # Add new permission

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.saunauser)
    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        queryset = self.queryset.filter(created_by=request.user.saunauser)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    # SaunaUser.user ist ein OneToOneField, daher select_related für Optimierung
    queryset = SaunaUser.objects.select_related('user').all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user.saunauser)
        return Response(serializer.data)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.select_related('sender').all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSenderOrAdminOrReadOnly] # Added IsSenderOrAdminOrReadOnly

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.saunauser)

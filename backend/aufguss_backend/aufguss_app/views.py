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

class AufgussViewSet(viewsets.ModelViewSet):
    queryset = AufgussSession.objects.all()
    serializer_class = AufgussSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.saunauser)
    @action(detail=False, methods=['get'])
    def my_sessions(self, request):
        queryset = self.queryset.filter(created_by=request.user.saunauser)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = SaunaUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user.saunauser)
        return Response(serializer.data)

class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.saunauser)

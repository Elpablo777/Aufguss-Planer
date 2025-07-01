from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, AufgussViewSet, ChatViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'aufguesse', AufgussViewSet)
router.register(r'chats', ChatViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls

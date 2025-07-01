from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AufgussViewSet, ChatViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'aufguesse', AufgussViewSet)
router.register(r'chats', ChatViewSet)

urlpatterns = router.urls

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FriendshipViewSet, FriendsViewSet, RegisterView

router = DefaultRouter()

router.register(r'friends', FriendsViewSet, basename='friends')
router.register(r'friendship', FriendshipViewSet, basename='friendship')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]

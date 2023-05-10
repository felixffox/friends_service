from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Friendship, StatusFriendship
from .serializers import (CustomUserRegisterSerializer, CustomUserSerializer,
                          FriendshipSerializer, FriendshipStatusSerializer)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserRegisterSerializer


class FriendsViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Friendship.objects.all()
    serializer_classes = {'list': CustomUserSerializer,
                          'retrieve': FriendshipStatusSerializer,
                          'create': FriendshipSerializer}
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """Список друзей"""
        return super(FriendsViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Отправить заявку в друзья"""
        serializer = FriendshipSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                CustomUser,
                pk=request.data.get('target_friend')
            )
            if request.user != user:
                response, stat = request.user.add_request_friendship(user)
                serializer = FriendshipSerializer(response)
                return Response(serializer.data, status=stat)
            return Response(
                {'detail': ErrorDetail("Нельзя отправить заявку самому себе.",
                code='bad_self_request')
            },status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Посмотреть статус дружбы"""
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        if request.user == user:
            status_string = "Это вы."
        if request.user != user:
            status_string = request.user.get_friendship_status(user)
        return Response(
            {'friendship_status': status_string}, 
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Удалить друга"""
        user = get_object_or_404(CustomUser, pk=kwargs['pk'])
        request.user.delete_friend(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        is_friend = StatusFriendship.ACCEPTED
        return self.request.user.get_users_friends(is_friend)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_classes.get(self.action, None)


class FriendshipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = FriendshipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status_friendship',)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """Список заявок"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Принять заявку в друзья"""
        friendship = get_object_or_404(Friendship, pk=kwargs['pk'])
        if friendship.initiator_friend == request.user \
        and friendship.status_friendship == StatusFriendship.INCOMING:
            friendship = friendship.accept_friendship()
            return Response(
                FriendshipSerializer(friendship).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"detail": ErrorDetail(
                "Попытка доступа к чужой или неактуальной заявке.",
                code='not_your_request'
            )
        },status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Отклонить заявку в друзья"""
        friendship = get_object_or_404(Friendship, pk=kwargs['pk'])
        if friendship.initiator_friend == request.user \
        and friendship.status_friendship == StatusFriendship.INCOMING:
            friendship.reject_friendship()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": ErrorDetail(
                "Попытка доступа к чужой или неактуальной заявке.",
                code='not_your_request'
            )
        },status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Friendship.objects.filter(initiator_friend=self.request.user)

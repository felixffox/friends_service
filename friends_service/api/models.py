from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusFriendship(models.TextChoices):
    NOT_REQUESTED = 'NR', _('Заявка не отправлена')
    OUTGOING = 'OU', _('Исходящая заявка')
    INCOMING = 'IN', _('Входящая заявка')
    PENDING = 'PE', _('Ожидается ответ')
    REJECTED = 'RE', _('Заявка отклонена')
    ACCEPTED = 'AC', _('Заявка принята')


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=50,
        unique=True,
        help_text='Обязательно для заполнения'
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Обязательно для заполнения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}'

    def add_request_friendship(self, user):
        """Отправить заявку в друзья"""
        if Friendship.objects.filter(
            initiator_friend=self,
            target_friend=user,
            status_friendship=StatusFriendship.ACCEPTED
        ):
            return Friendship.objects.get(
                initiator_friend=self,
                target_friend=user,
                status_friendship=StatusFriendship.ACCEPTED
            ), 208

        if Friendship.objects.filter(
            initiator_friend=self,
            target_friend=user,
            status_friendship=StatusFriendship.OUTGOING
        ):
            return Friendship.objects.get(
                initiator_friend=self,
                target_friend=user,
                status_friendship=StatusFriendship.OUTGOING
            ), 208

        if Friendship.objects.filter(
            initiator_friend=self,
            target_friend=user,
            status_friendship=StatusFriendship.INCOMING
        ):
            Friendship.objects.filter(
                initiator_friend__in=[self, user],
                target_friend__in=[user, self]
            ).update(
                status_friendship=StatusFriendship.ACCEPTED
                )

            return Friendship.objects.get(
                initiator_friend=self,
                target_friend=user,
                status_friendship=StatusFriendship.ACCEPTED
            ), 200

        instance = Friendship.objects.create(
            initiator_friend=self,
            target_friend=user,
            status_friendship=StatusFriendship.OUTGOING
        )
        Friendship.objects.create(
            initiator_friend=user,
            target_friend=self,
            status_friendship=StatusFriendship.INCOMING
        )
        return instance, 201

    def delete_friend(self, user):
        """Удалить из друзей"""
        friendships = Friendship.objects.filter(
            initiator_friend__in=[self, user],
            target_friend__in=[user, self],
            status_friendship=StatusFriendship.ACCEPTED
        )
        if friendships:
            friendships.delete()

    def get_users_friends(self, is_friend):
        """Получить список друзей или список пользователей, \
        которые отправили/получили заявки от пользователя"""
        is_friend = StatusFriendship.ACCEPTED
        friends_id = Friendship.objects.filter(
            initiator_friend=self,
            status_friendship=is_friend
        ).values_list('target_friend__id', flat=True)
        return CustomUser.objects.filter(id__in=friends_id)

    def get_friendship_request(self, in_out):
        """Получить список заявок в друзья \
        (полученных/отправленных/принятых)"""
        return Friendship.objects.filter(
            initiator_friend=self,
            status_friendship=in_out
        )

    def get_friendship_status(self, user):
        """Получить статус дружбы с пользователем"""
        relation = Friendship.objects.filter(
            initiator_friend=self,
            target_friend=user
        )
        if relation.exists():
            return relation[0].status_friendship


class Friendship(models.Model):
    """Модель отношений между юзерами - друзья"""
    initiator_friend = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='initiator_friend',
        verbose_name='Отправитель заявки',
        null=False
    )
    target_friend = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='target_friend',
        verbose_name='Получатель заявки',
        null=False
    )
    status_friendship = models.CharField(
        max_length=2,
        choices=StatusFriendship.choices,
        default=StatusFriendship.NOT_REQUESTED,
        null=False
    )
    friendship_date = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        constraints = [
            models.UniqueConstraint(fields=['initiator_friend', 'target_friend'],
                                    name='unique_friendship')
        ]

    def __str__(self) -> str:
        return f'{self.initiator_friend.username} и \
        {self.target_friend.username} - {self.status_friendship}'

    def accept_friendship(self):
        """Принять заявку в друзья"""
        Friendship.objects.filter(
            initiator_friend__in=[self.initiator_friend, self.target_friend],
            target_friend__in=[self.target_friend, self.initiator_friend]
        ).update(status_friendship=StatusFriendship.ACCEPTED)

        return Friendship.objects.get(
            initiator_friend=self.initiator_friend,
            target_friend=self.target_friend,
            status_friendship=StatusFriendship.ACCEPTED
        )

    def reject_friendship(self):
        """Отклонить заявку в друзья"""
        Friendship.objects.filter(
            initiator_friend__in=[self.initiator_friend, self.target_friend],
            target_friend__in=[self.target_friend, self.initiator_friend]
        ).delete()
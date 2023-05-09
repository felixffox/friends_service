from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
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


class Friendship(models.Model):
    """Модель отношений между юзерами - друзья"""
    initiator_friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='initiator_friend',
        verbose_name='Отправитель заявки',
        null=False
    )
    target_friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='target_friend',
        verbose_name='Получатель заявки',
        null=False
    )
    
    class StatusFriendship(models.TextChoices):
        NOT_REQUESTED = 'NR', _('Заявка не отправлена')
        PENDING = 'PE', _('Ожидается ответ')
        REJECTED = 'RE', _('Заявка отклонена')
        ACCEPTED = 'AC', _('Заявка принята')

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

from django.contrib.auth.models import AbstractUser
from django.db import models


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
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend',
    )
    second_friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='second_friend'
    )
    status = models.CharField()
    friendship_date = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        constraints = [
            models.UniqueConstraint(fields=['friend', 'second_friend'],
                                    name='unique_friendship')
        ]

    def __str__(self) -> str:
        return f'{self.friend.username} и \
        {self.second_friend.username} друзья!'

#class FriendRequest(models.Model):
#    """Модель заявки на добавление в друзья"""
#    send_user = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='send_user'
#    )
#    receive_user = models.ForeignKey(
#        User,
#        on_delete=models.CASCADE,
#        related_name='receive_user'
#    )
#    request_date = models.DateTimeField(auto_now_add=True)
#
#    class Meta:
#        verbose_name = 'Заявка'
#        verbose_name_plural = 'Заявки'
#        constraints = [
#            models.UniqueConstraint(fields=['send_user', 'receive_user'],
#                                    name='unique_request')
#        ]
#
#    def __str__(self) -> str:
#        return f'Заявка на добавление в друзья: \
#        {self.send_user.username} -> {self.receive_user.username}'
#    pass
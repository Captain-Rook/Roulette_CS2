from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    """Модель пользователя"""
    username = models.CharField(
        verbose_name='Имя пользователя из steam',
        max_length=32,
        unique=True
    )
    steam_id = models.CharField(
        verbose_name='Идентификатор steam аккаунта пользователя',
        max_length=17,
        unique=True
    )
    steam_profile_url = models.URLField(
        verbose_name='Ссылка на steam профиль пользователя',
    )
    avatar = models.URLField(
        verbose_name='Ссылка на аватар пользователя в steam',
        blank=True,
        null=True,
    )
    balance = models.DecimalField(
        verbose_name='Баланс игровой валюты',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    trade_url = models.URLField(
        verbose_name='Трейд-ссылка',
        blank=True,
        null=True,
        unique=True,
        default=None
    )

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username} (SteamID: {self.steam_id})"

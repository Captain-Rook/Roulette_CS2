from django.contrib.auth import get_user_model
from django.db import models

from core import constants

User = get_user_model()


class Skin(models.Model):
    weapon = models.CharField(
        verbose_name='Название оружия',
        max_length=constants.LENGTH_CHAR_FIELDS
    )
    fullname = models.CharField(
        verbose_name='Название скина',
        max_length=constants.LENGTH_CHAR_FIELDS,
        unique=True
    )
    skin_image = models.ImageField(
        verbose_name='Картинка скина',
        upload_to='skin/media/',
        null=True,
        blank=True
    )
    price = models.IntegerField(verbose_name='Цена скина')
    rare = models.CharField(max_length=16, default=None, null=True)

    class Meta:
        verbose_name = 'скин'
        verbose_name_plural = 'Скины'


class Case(models.Model):
    name = models.CharField(
        verbose_name='Название кейса',
        max_length=constants.LENGTH_CHAR_FIELDS,
        unique=True
    )
    price = models.PositiveIntegerField(verbose_name='Цена кейса')
    skins = models.ManyToManyField(
        verbose_name='Скины',
        to=Skin,
        through='CaseSkin',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='case/media/',
        verbose_name='Картинка кейса',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'кейс'
        verbose_name_plural = 'Кейсы'
        default_related_name = 'cases'


class CaseSkin(models.Model):
    case_id = models.ForeignKey(
        verbose_name='Кейс',
        to=Case,
        on_delete=models.CASCADE,
    )
    skin_id = models.ForeignKey(
        verbose_name='Скин',
        to=Skin,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'case_skins'


class SkinTransaction(models.Model):
    """Модель операций со скинами"""
    ACTION_CHOICES = (
        (constants.ACTION_SALED, "Продан"),
        (constants.ACTION_USED_IN_UPGRADE, "Использован в апгрейде"),
        (constants.ACTION_USED_IN_CONTRACT, "Использован в контракте"),
        (constants.ACTION_DISPLAYED_IN_STEAM, 'Выведен в Steam'),
        (constants.ACTION_CHANGED, 'Заменен на другой'),
        (constants.ACTION_NONE, "Нет действий"),
    )
    SOURCE_CHOICES = (
        (constants.SOURCE_CASE, "Кейс"),
        (constants.SOURCE_FREE_CASE, "Бесплатный кейс"),
        (constants.SOURCE_UPGRADE, "Апгрейд"),
        (constants.SOURCE_CONTRACT, "Контракт"),
        (constants.SOURCE_PRESENT, "Подарок"),
        (constants.SOURCE_CHANGE, 'Замена'),
    )
    STATUS_CHOICES = (
        (constants.STATUS_IN_INVENTORY, 'В инвентаре'),
        (constants.STATUS_IN_PROCESS_TO_OUTPUT, 'В процессе на вывод'),
        (constants.STATUS_OUTPUT_ERROR, 'Ошибка вывода'),
        (constants.STATUS_SUCCESS_OUTPUT, 'Успешно выведен в steam'),
        (constants.STATUS_USED_IN_CONTRACT, 'Использован в контракте'),
        (constants.STATUS_CHANGED, 'Заменен на другой'),
        (constants.STATUS_USED_IN_UPGRADE, 'Использован в апгрейде'),
        (constants.STATUS_SALED, 'Продан'),
    )

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE
    )
    skin = models.ForeignKey(
        verbose_name='Скин',
        to=Skin,
        on_delete=models.DO_NOTHING
    )
    source = models.CharField(
        verbose_name='Источник получения скина',
        choices=SOURCE_CHOICES,
        max_length=max([len(choice) for choice, _ in SOURCE_CHOICES]),
        default=constants.SOURCE_CASE
    )
    action = models.CharField(
        verbose_name='Действие со скином',
        choices=ACTION_CHOICES,
        max_length=max([len(choice) for choice, _ in ACTION_CHOICES]),
        default=constants.ACTION_NONE,
    )
    status = models.CharField(
        verbose_name='Состояние скина',
        choices=STATUS_CHOICES,
        max_length=max([len(choice) for choice, _ in STATUS_CHOICES]),
        default=constants.STATUS_IN_INVENTORY,
    )
    details = models.JSONField(
        verbose_name='Детали операции',
        blank=True,
    )
    get_at = models.DateTimeField(
        verbose_name='Дата и время получения скина',
        auto_now_add=True,
    )
    used_at = models.DateTimeField(
        verbose_name='Дата и время использования скина',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-get_at',)
        verbose_name = 'транзакция'
        verbose_name_plural = 'Транзакции'
        default_related_name = 'skin_transactions'
